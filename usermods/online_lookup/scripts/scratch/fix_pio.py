with open("platformio_override.ini", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == "extends = env:esp32c3dev":
        new_lines.append("extends = esp32c3\n") # Or just remove it? Actually let's look at platformio.ini to see what it should extend.
    else:
        new_lines.append(line)

with open("platformio_override.ini", "w") as f:
    f.writelines(new_lines)
