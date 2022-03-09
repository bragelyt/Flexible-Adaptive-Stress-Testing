from af_colav_sim.models.controllers.steerable_vessel_controller import SteerableVesselController

class AdversarialRouter:

    def __init__(self, controller, route) -> None:
        self.controller : SteerableVesselController = controller
        self.route = route
        self.nu_d = None
        self.i = 0

    def step(self):
        if self.i < len(self.route):
            self.nu_d = self.route[self.i]
            self.i += 1
        else:
            self.nu_d = [1., 0., 0.]
        self.controller.update_nu_d(self.nu_d)

