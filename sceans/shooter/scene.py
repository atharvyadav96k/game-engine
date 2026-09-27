import pygame
from time import time

from physics.physics_system import PhysicsSystem
from physics.collsion_system import CollisionSystem
from display.screen.screen import Screen
from display.elements.rectangle.rectangle import Rectangle
from display.elements.text.text import Text
from display.elements.button.button import Button
from display.styles.style import Style
from display.styles.stylepproperties import Property

from . import constants as c
from .levels import LEVELS, build_level
from .weapons import WeaponSystem
from .entities.player import Player
from .entities.enemy import Enemy


class ShooterGame(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.children.append(Button(self.display, "pause", "II", (10, 10)))

        self._next_id = 0
        self.game_objects = []
        self.collisionSystem = CollisionSystem(self.game_objects)
        self.physics = PhysicsSystem(self.game_objects, gravity=(0, 980.0))
        self.weapons = WeaponSystem(self.display, self._gen_id, self.game_objects)

        self.prev_time = time()
        self.delta = 1 / 60

        data = self.screenManager.getRouteData() or {}
        start_level = 0
        raw_level = data.get("level")
        if raw_level is not None and str(raw_level).isdigit():
            start_level = max(0, min(len(LEVELS) - 1, int(raw_level) - 1))

        self._load_level(start_level)

    def _gen_id(self, prefix):
        self._next_id += 1
        return f"{prefix}-{self._next_id}"

    def _load_level(self, index):
        self.game_objects.clear()
        self.weapons.reset()
        self.level_index = index

        self.platforms, player_spawn, enemy_spawns = build_level(self.display, LEVELS[index], self._gen_id)
        self.game_objects.extend(self.platforms)

        self.player = Player(self.display, player_spawn, self._gen_id)
        self.game_objects.append(self.player.go)

        self.enemies = [Enemy(self.display, spawn, self._gen_id) for spawn in enemy_spawns]
        self.game_objects.extend(e.go for e in self.enemies)

        self.state = "playing"

    def inputs(self, events):
        super().inputs(events)

        if self.state != "playing":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if self.state == "level_complete" and event.key == pygame.K_RETURN:
                        if self.level_index + 1 < len(LEVELS):
                            self._load_level(self.level_index + 1)
                        else:
                            self.state = "game_won"
                    elif self.state in ("dead", "game_won") and event.key == pygame.K_r:
                        self._load_level(0 if self.state == "game_won" else self.level_index)
            return

        wants_bomb = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 3 for e in events)

        self.player.tick_cooldowns(self.delta)
        self.player.update_ground_state(self.platforms)

        keys = pygame.key.get_pressed()
        self.player.handle_movement(keys, self.delta)

        aim = self.player.aim_dir(pygame.mouse.get_pos())

        if pygame.mouse.get_pressed()[0] and self.player.can_fire_gun():
            self.weapons.fire_player_bullet(self.player.center(), aim)
            self.player.register_gun_fire()

        if wants_bomb and self.player.can_throw_bomb():
            self.weapons.throw_bomb(self.player.center(), aim)
            self.player.register_bomb_throw()

    def _update_enemy_ai(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                continue
            enemy.patrol()
            direction = enemy.try_get_shot_direction(self.player, self.platforms, self.delta)
            if direction is not None:
                self.weapons.fire_enemy_bullet(enemy.center(), direction)

    def update(self):
        current_time = time()
        self.delta = min(current_time - self.prev_time, 1 / 20)
        self.prev_time = current_time

        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "pause":
                    self.screenManager.route("level-screen")

        if self.state != "playing":
            return

        self._update_enemy_ai()

        self.physics.update(self.delta)
        self.player.clamp_velocity()
        self.collisionSystem.update()

        self.weapons.update(self.delta, self.collisionSystem, self.player, self.enemies)

        for enemy in self.enemies:
            if not enemy.is_alive() and enemy.go in self.game_objects:
                self.game_objects.remove(enemy.go)
        self.enemies = [e for e in self.enemies if e.is_alive()]

        if not self.player.is_alive():
            self.state = "dead"
            return

        if len(self.enemies) == 0:
            self.state = "level_complete"

    def _render_bar(self, x, y, w, h, ratio, color):
        Rectangle(self.display, "", (x, y), (w, h),
                  Style({Property.BACKGROUND: (40, 40, 40)})).render()
        fill_w = max(0, int(w * max(0.0, min(1.0, ratio))))
        if fill_w > 0:
            Rectangle(self.display, "", (x, y), (fill_w, h),
                      Style({Property.BACKGROUND: color})).render()

    def _render_hud(self):
        Text(self.display, "", f"Level {self.level_index + 1}/{len(LEVELS)}", (20, 20),
             Style({Property.FONT_SIZE: 24, Property.COLOR: (255, 255, 255)})).render()
        Text(self.display, "", f"Enemies: {len(self.enemies)}", (20, 50),
             Style({Property.FONT_SIZE: 20, Property.COLOR: (255, 200, 200)})).render()

        self._render_bar(20, 80, 220, 16, self.player.hp / c.PLAYER_MAX_HP, (200, 40, 40))
        self._render_bar(20, 100, 220, 10, self.player.fuel / c.FUEL_MAX, (60, 160, 220))
        Text(self.display, "", f"Ammo: {self.player.ammo}", (20, 120),
             Style({Property.FONT_SIZE: 18, Property.COLOR: (255, 230, 80)})).render()
        Text(self.display, "", f"Bombs: {self.player.bomb_count}", (20, 145),
             Style({Property.FONT_SIZE: 18, Property.COLOR: (120, 220, 120)})).render()

        if self.state == "level_complete":
            Text(self.display, "", "Level Complete! Press ENTER to continue",
                 (c.ARENA_W // 2 - 280, c.ARENA_H // 2 - 20),
                 Style({Property.FONT_SIZE: 30, Property.COLOR: (255, 255, 255)})).render()
        elif self.state == "dead":
            Text(self.display, "", "You Died - Press R to retry",
                 (c.ARENA_W // 2 - 220, c.ARENA_H // 2 - 20),
                 Style({Property.FONT_SIZE: 30, Property.COLOR: (255, 80, 80)})).render()
        elif self.state == "game_won":
            Text(self.display, "", "You Win! All levels cleared - Press R to play again",
                 (c.ARENA_W // 2 - 340, c.ARENA_H // 2 - 20),
                 Style({Property.FONT_SIZE: 30, Property.COLOR: (255, 255, 255)})).render()

    def render(self):
        for go in self.game_objects:
            go.render()
        self.weapons.render(self.display)
        self._render_hud()
        super().render()
