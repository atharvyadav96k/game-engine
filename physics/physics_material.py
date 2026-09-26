class PhysicsMaterial():
    def __init__(self, restitution=0.0, friction=0.5):
        self.restitution = restitution
        self.friction = friction

    @staticmethod
    def combine(material_a, material_b):
        restitution = max(material_a.restitution, material_b.restitution)
        friction = (material_a.friction * material_b.friction) ** 0.5
        return PhysicsMaterial(restitution, friction)
