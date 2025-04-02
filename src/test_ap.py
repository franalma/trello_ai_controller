
from drone.tello_ctr import HCTrelloController


drone = HCTrelloController()
drone.init(False)
drone.connect_ap()