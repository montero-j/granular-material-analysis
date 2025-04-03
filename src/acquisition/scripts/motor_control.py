#!/usr/bin/env python3

import time


def motor1(IN1, IN2, IN3, IN4, parlante):
    """
    Controla el motor paso a paso conectado a Arduino para realizar un movimiento específico.

    Args:
        IN1: Pin de control IN1 del motor.
        IN2: Pin de control IN2 del motor.
        IN3: Pin de control IN3 del motor.
        IN4: Pin de control IN4 del motor.
        parlante: Pin de control del parlante.

    Returns:
        0: Si el movimiento del motor se completó correctamente.
    """
    # movimiento del motor
    m = 0  # el giro es hacia adelante
    parlante.write(0)

    while m < 35:
        IN4.write(1)
        IN3.write(1)
        IN2.write(0)
        IN1.write(0)
        time.sleep(0.05)

        IN4.write(0)
        IN3.write(1)
        IN2.write(1)
        IN1.write(0)
        time.sleep(0.05)

        IN4.write(0)
        IN3.write(0)
        IN2.write(1)
        IN1.write(1)
        time.sleep(0.05)

        IN4.write(1)
        IN3.write(0)
        IN2.write(0)
        IN1.write(1)
        time.sleep(0.05)

        m += 1

    time.sleep(5)

    return 0
    
def motor2(IN1, IN2, IN3, IN4, parlante):
    """
    Controla el motor paso a paso conectado a Arduino para realizar un movimiento específico.

    Args:
        IN1: Pin de control IN1 del motor.
        IN2: Pin de control IN2 del motor.
        IN3: Pin de control IN3 del motor.
        IN4: Pin de control IN4 del motor.
        parlante: Pin de control del parlante.

    Returns:
        0: Si el movimiento del motor se completó correctamente.
    """
    k = 0 # el giro es hacia atras
    parlante.write(0)
    
    while k < 35:
        IN4.write(1)
        IN3.write(1)
        IN2.write(0)
        IN1.write(0)
        time.sleep(0.05)

        IN4.write(0)
        IN3.write(1)
        IN2.write(1)
        IN1.write(0)
        time.sleep(0.05)

        IN4.write(0)
        IN3.write(0)
        IN2.write(1)
        IN1.write(1)
        time.sleep(0.05)

        IN4.write(1)
        IN3.write(0)
        IN2.write(0)
        IN1.write(1)
        time.sleep(0.05)

        k += 1

    time.sleep(5)


if __name__ == "__main__":
	motor1()
	motor2()
