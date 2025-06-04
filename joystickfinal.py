from machine import Pin, ADC, PWM
import time
import random

# === Joystick 設定 ===
joy_x = ADC(Pin(34))
joy_y = ADC(Pin(35))
joy_x.atten(ADC.ATTN_11DB)
joy_y.atten(ADC.ATTN_11DB)

# === LED 腳位 ===
led_gpio_list = [16, 17, 18, 19, 23, 5, 2, 22]
led_pins = [Pin(i, Pin.OUT) for i in led_gpio_list]

# === 馬達風扇控制 ===
fan = PWM(Pin(27), freq=1000)
fan.duty(0)

# === 遊戲變數 ===
current_pos = 0
target_pos = random.randint(0, 7)

countdown_seconds = 10
last_tick = time.ticks_ms()

def show_led(pos, target):
    for i, led in enumerate(led_pins):
        if i == pos and i == target:
            led.value(1)
        elif i == target:
            led.value(1)
        elif i == pos:
            led.value(1)
        else:
            led.value(0)

def read_joystick():
    x = joy_x.read()
    if x < 1000:
        return -1  # 向左
    elif x > 3000:
        return 1   # 向右
    else:
        return 0   # 中間

def trigger_fan(on):
    if on:
        fan.duty(500)
    else:
        fan.duty(0)

# === 遊戲主迴圈 ===
while True:
    dx = read_joystick()
    if dx != 0:
        current_pos = (current_pos + dx) % 8
        show_led(current_pos, target_pos)
        time.sleep(0.2)

    show_led(current_pos, target_pos)

    # === 檢查是否成功對準 ===
    if current_pos == target_pos:
        print("✅ 找到目標！")
        for _ in range(3):
            led_pins[current_pos].value(0)
            time.sleep(0.1)
            led_pins[current_pos].value(1)
            time.sleep(0.1)

        # 重設目標與倒數
        target_pos = random.randint(0, 7)
        countdown_seconds = 10
        last_tick = time.ticks_ms()
        trigger_fan(False)

    # === 倒數時間邏輯 ===
    now = time.ticks_ms()
    if time.ticks_diff(now, last_tick) >= 1000:
        countdown_seconds -= 1
        last_tick = now
        print("⏳ 倒數：", countdown_seconds, "秒")

    if countdown_seconds <= 0:
        print("❌ 時間到！風扇啟動！")
        trigger_fan(True)
    else:
        trigger_fan(False)

    time.sleep(0.05)
