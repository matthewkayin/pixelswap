from PIL import Image

instructions_file = open("config.txt", "r")
instructions = instructions_file.readlines()

file_names = []
pixel_rules = []

for instruction in instructions:
    if instruction.startswith("("):
        instruction = instruction[:instruction.index("\n")]
        r = instruction[instruction.index("(") + 1:instruction.index(",")]
        instruction = instruction[instruction.index(",") + 1:]
        g = instruction[:instruction.index(",")]
        instruction = instruction[instruction.index(",") + 1:]
        b = instruction[:instruction.index(")")]
        new_r = instruction[instruction.index("(") + 1:instruction.index(",")]
        instruction = instruction[instruction.index(",") + 1:]
        new_g = instruction[:instruction.index(",")]
        instruction = instruction[instruction.index(",") + 1:]
        new_b = instruction[:instruction.index(")")]

        pixel_rules.append([(int(r), int(g), int(b)), (int(new_r), int(new_g), int(new_b))])
    else:
        file_names.append([instruction[:instruction.index("-")], instruction[instruction.index(">") + 1:instruction.index("\n")]])

for i in range(0, len(file_names)):
    source_image_path = file_names[i][0]
    dest_image_path = file_names[i][1]

    source_image = Image.open(source_image_path)
    width, height = source_image.size
    dest_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    for x in range(0, width):
        for y in range(0, height):
            r, g, b, a = source_image.getpixel((x, y))
            used_rule = False
            for pixel_rule in pixel_rules:
                if r == pixel_rule[0][0] and g == pixel_rule[0][1] and b == pixel_rule[0][2]:
                    dest_image.putpixel((x, y), (pixel_rule[1][0], pixel_rule[1][1], pixel_rule[1][2], a))
                    used_rule = True
                    break
            if not used_rule:
                dest_image.putpixel((x, y), (r, g, b, a))

    dest_image.save(dest_image_path, 'PNG')
