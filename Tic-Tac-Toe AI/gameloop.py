
team1 = True

def check_input(event, cells, screen):
    global team1
    for c in cells:
        if (c.position.x * screen.get_width() / 3 < event["pos"][0] < c.position.x * screen.get_width() / 3 + screen.get_width() / 3
            and c.position.y * screen.get_height() / 3 < event["pos"][1] < c.position.y * screen.get_height() / 3 + screen.get_height() / 3):
            if team1 and c.cell_type == 0:
                c.cell_type = 1
                team1 = not team1
            if not team1 and c.cell_type == 0:
                c.cell_type = 2
                team1 = not team1

def check_victory(cells):
    for i in range(9):
        if i+2 < 9 and cells[i].position.y == cells[i+1].position.y == cells[i+2].position.y and cells[i].cell_type == cells[i+1].cell_type == cells[i+2].cell_type != 0:
            return [cells[i].position, cells[i+2].position, cells[i].cell_type]
        elif i+6 < 9 and cells[i].position.x == cells[i+3].position.x == cells[i+6].position.x and cells[i].cell_type == cells[i+3].cell_type == cells[i+6].cell_type != 0:
            return [cells[i].position, cells[i+6].position, cells[i].cell_type]
        elif i+8 < 9 and cells[i].position.y != cells[i+4].position.y != cells[i+8].position.y and cells[i].cell_type == cells[i+4].cell_type == cells[i+8].cell_type != 0:
            return [cells[i].position, cells[i+8].position, cells[i].cell_type]
        elif i+4 < 9 and cells[i].position.y != cells[i+2].position.y != cells[i+4].position.y and cells[i].cell_type == cells[i+2].cell_type == cells[i+4].cell_type != 0:
            return [cells[i].position, cells[i+4].position, cells[i].cell_type]
    return [[-1, -1],[-1, -1], 0]