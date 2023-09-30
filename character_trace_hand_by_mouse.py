from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand = load_image('hand_arrow.png')

def handle_events():
    global running
    global mouse_x, mouse_y
    global hand_positions

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, TUK_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                hand_positions.append((mouse_x, mouse_y))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def move_in_line():
    global player_first_x, player_first_y
    global player_last_x, player_last_y
    global character_x, character_y
    global i, a
    global toward_hand

    if toward_hand:
        if a < len(hand_positions):
            if player_first_x == player_last_x and player_first_y == player_last_y:
                for x, y in hand_positions[a:a+1]:
                    player_last_x, player_last_y = x, y

            t = i / 100
            character_x = (1 - t) * player_first_x + t * player_last_x
            character_y = (1 - t) * player_first_y + t * player_last_y
            i += 1
            if i > 100:
                i = 0
                a += 1
                toward_hand = False



running = True
toward_hand = False

mouse_x, mouse_y = TUK_WIDTH // 2, TUK_HEIGHT // 2
character_x, character_y = TUK_WIDTH // 2, TUK_HEIGHT // 2
player_first_x, player_first_y = character_x, character_y
player_last_x, player_last_y = character_x, character_y
hand_positions = []

i = 0
a = 0
frame = 0
hide_cursor()

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    hand.draw(mouse_x, mouse_y)
    character.clip_draw(frame * 100, 100 * 1, 100, 100, character_x, character_y)

    if character_x == player_last_x and character_y == player_last_y:
        player_first_x, player_first_y = player_last_x, player_last_y
        toward_hand = True
    for x, y in hand_positions:
        hand.draw(x, y)

    move_in_line()
    update_canvas()

    frame = (frame + 1) % 8
    handle_events()
    delay(0.01)

close_canvas()