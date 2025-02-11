from wheelgear2 import MotorController  
# MotorController 클래스를 file1에서 임포트

controller = MotorController(port='/dev/ttyACM0')

# controller.id_set(0x01)
controller.id_query()

# controller.query_velocity_and_angle(0x01)

# controller.switch_current_mode(0x01)
# controller.switch_velocity_mode(0x01)
# controller.switch_angle_mode(0x01)

# controller.set_velocity(0x01, 10)
# controller.set_angle(0x01, 30)
# controller.set_relative_angle(0x01, 100)

controller.brake(0x01)