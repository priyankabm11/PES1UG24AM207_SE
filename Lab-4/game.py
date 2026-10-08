import pygame
import random

TILE = 40
COLS, ROWS = 20, 15

WALL, FLOOR, CHEST, KEY, TRAP = 0, 1, 2, 3, 4

SPEED = 3
GUARD_SPEED = 2


WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + 50
FPS = 60


def generate_world():
    grid = [[WALL] * COLS for _ in range(ROWS)]
    rooms = []

    # Generate rooms
    for _ in range(12):
        w = random.randint(3, 6)
        h = random.randint(3, 5)

        x = random.randint(1, COLS - w - 1)
        y = random.randint(1, ROWS - h - 1)

        room = pygame.Rect(x, y, w, h)

        overlap = any(
            room.inflate(2, 2).colliderect(r)
            for r in rooms
        )

        if not overlap:
            rooms.append(room)

            for ry in range(y, y + h):
                for rx in range(x, x + w):
                    grid[ry][rx] = FLOOR

    # Make sure there are enough rooms
    if len(rooms) < 4:
        return generate_world()

    # Connect rooms
    for i in range(len(rooms) - 1):
        ax, ay = rooms[i].centerx, rooms[i].centery
        bx, by = rooms[i + 1].centerx, rooms[i + 1].centery

        # Horizontal corridor
        cx = ax

        while cx != bx:
            grid[ay][cx] = FLOOR
            cx += 1 if bx > cx else -1

        # Vertical corridor
        cy = ay

        while cy != by:
            grid[cy][bx] = FLOOR
            cy += 1 if by > cy else -1

    # Put chest and key in the last two rooms
    chest_room = rooms[-1]
    key_room = rooms[-2]

    chest_r = chest_room.centery
    chest_c = chest_room.centerx

    key_r = key_room.centery
    key_c = key_room.centerx

    grid[chest_r][chest_c] = CHEST
    grid[key_r][key_c] = KEY

    # Starting room
    start = rooms[0]

    # ------------------------------------------------
    # TASK 1: ADD FLOOR TRAPS
    # ------------------------------------------------

    trap_candidates = []

    for r in range(ROWS):
        for c in range(COLS):

            if grid[r][c] != FLOOR:
                continue

            # Do not put traps inside starting room
            if start.collidepoint(c, r):
                continue

            # Do not put traps on key/chest
            if (r, c) in [
                (key_r, key_c),
                (chest_r, chest_c)
            ]:
                continue

            trap_candidates.append((r, c))

    # Make sure there are enough trap locations
    if len(trap_candidates) < 5:
        return generate_world()

    random.shuffle(trap_candidates)

    # Place exactly 5 traps
    for r, c in trap_candidates[:5]:
        grid[r][c] = TRAP

    return grid, start


COLORS = {
    WALL: (60, 50, 70),
    FLOOR: (200, 190, 170),
    CHEST: (200, 160, 30),
    KEY: (220, 220, 60),
    TRAP: (180, 70, 70),
}


class Player:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.color = (60, 120, 220)
        self.has_key = False

    def move(self, keys, grid, rows, cols):

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -SPEED

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = SPEED

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -SPEED

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = SPEED

        self._try_move(
            dx,
            0,
            grid,
            rows,
            cols
        )

        self._try_move(
            0,
            dy,
            grid,
            rows,
            cols
        )

    def _try_move(self, dx, dy, grid, rows, cols):

        new = self.rect.move(dx, dy)

        corners = [
            (new.left, new.top),
            (new.right - 1, new.top),
            (new.left, new.bottom - 1),
            (new.right - 1, new.bottom - 1),
        ]

        for px, py in corners:

            c = px // TILE
            r = py // TILE

            if (
                not (0 <= r < rows and 0 <= c < cols)
                or grid[r][c] == WALL
            ):
                return

        self.rect = new

    def draw(self, screen):

        pygame.draw.ellipse(
            screen,
            self.color,
            self.rect
        )

        # Show key indicator after collecting key
        if self.has_key:

            pygame.draw.circle(
                screen,
                (220, 220, 60),
                (
                    self.rect.right - 6,
                    self.rect.top + 6
                ),
                5
            )


# ====================================================
# TASK 2: ENEMY GUARD
# ====================================================

class Guard:

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            28,
            28
        )

        self.color = (180, 50, 50)

        self.direction = random.choice([
            (GUARD_SPEED, 0),
            (-GUARD_SPEED, 0),
            (0, GUARD_SPEED),
            (0, -GUARD_SPEED)
        ])

    def move(self, grid, rows, cols):

        dx, dy = self.direction

        new = self.rect.move(
            dx,
            dy
        )

        corners = [
            (new.left, new.top),
            (new.right - 1, new.top),
            (new.left, new.bottom - 1),
            (new.right - 1, new.bottom - 1),
        ]

        blocked = False

        for px, py in corners:

            c = px // TILE
            r = py // TILE

            if (
                not (0 <= r < rows and 0 <= c < cols)
                or grid[r][c] == WALL
            ):
                blocked = True
                break

        if blocked:

            # Choose another direction
            self.direction = random.choice([
                (GUARD_SPEED, 0),
                (-GUARD_SPEED, 0),
                (0, GUARD_SPEED),
                (0, -GUARD_SPEED)
            ])

        else:

            self.rect = new

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=6
        )

        # Guard eyes
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                self.rect.left + 8,
                self.rect.top + 9
            ),
            3
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                self.rect.left + 20,
                self.rect.top + 9
            ),
            3
        )


class GameEngine:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Treasure Hunt"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "monospace",
            24
        )

        self.big_font = pygame.font.SysFont(
            "monospace",
            40,
            bold=True
        )

        self.reset()

    def reset(self):

        self.grid, start = generate_world()

        # Starting position
        if start:

            sx = start.x * TILE + 6
            sy = start.y * TILE + 6

        else:

            sx = TILE + 6
            sy = TILE + 6

        self.player = Player(
            sx,
            sy
        )

        # ------------------------------------------------
        # Store exact starting position
        # ------------------------------------------------

        self.start_pos = (
            sx,
            sy
        )

        # ------------------------------------------------
        # TASK 2: CREATE GUARD
        # ------------------------------------------------

        guard_candidates = []

        for r in range(ROWS):
            for c in range(COLS):

                # Guard must be on normal floor
                if self.grid[r][c] != FLOOR:
                    continue

                # Do not spawn inside starting room
                if start and start.collidepoint(c, r):
                    continue

                # Keep guard away from starting position
                distance_from_start = (
                    abs(c - start.centerx)
                    + abs(r - start.centery)
                )

                if distance_from_start < 6:
                    continue

                guard_candidates.append(
                    (r, c)
                )

        if guard_candidates:

            gr, gc = random.choice(
                guard_candidates
            )

            gx = gc * TILE + 6
            gy = gr * TILE + 6

            self.guard = Guard(
                gx,
                gy
            )

        else:

            self.guard = None

        self.won = False

        self.status = (
            "Find the KEY, then the CHEST!"
        )

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                self.reset()

        return True

    def update(self):

        if self.won:
            return

        # ------------------------------------------------
        # PLAYER MOVEMENT
        # ------------------------------------------------

        keys = pygame.key.get_pressed()

        self.player.move(
            keys,
            self.grid,
            ROWS,
            COLS
        )

        # ------------------------------------------------
        # TASK 2: GUARD MOVEMENT
        # ------------------------------------------------

        if self.guard:

            self.guard.move(
                self.grid,
                ROWS,
                COLS
            )

            # Check collision between player and guard
            if self.player.rect.colliderect(
                self.guard.rect
            ):

                self.player.rect.topleft = (
                    self.start_pos
                )

                self.status = (
                    "Guard caught you! Back to start!"
                )

        # ------------------------------------------------
        # CHECK PLAYER'S CURRENT TILE
        # ------------------------------------------------

        pr = (
            self.player.rect.centery
            // TILE
        )

        pc = (
            self.player.rect.centerx
            // TILE
        )

        if 0 <= pr < ROWS and 0 <= pc < COLS:

            cell = self.grid[pr][pc]

            # ============================================
            # TASK 1: FLOOR TRAP
            # ============================================

            if cell == TRAP:

                # Return player to exact starting position
                self.player.rect.topleft = (
                    self.start_pos
                )

                self.status = (
                    "Trap! Back to start!"
                )

            # ============================================
            # KEY
            # ============================================

            elif cell == KEY:

                self.player.has_key = True

                # Remove key after collecting it
                self.grid[pr][pc] = FLOOR

                self.status = (
                    "Got the key! Find the CHEST!"
                )

            # ============================================
            # CHEST
            # ============================================

            elif (
                cell == CHEST
                and self.player.has_key
            ):

                self.won = True

                self.status = (
                    "Treasure found!"
                )

    def draw(self):

        self.screen.fill(
            (30, 25, 40)
        )

        # ------------------------------------------------
        # DRAW DUNGEON
        # ------------------------------------------------

        for r in range(ROWS):

            for c in range(COLS):

                cell = self.grid[r][c]

                rect = pygame.Rect(
                    c * TILE,
                    r * TILE,
                    TILE,
                    TILE
                )

                pygame.draw.rect(
                    self.screen,
                    COLORS[cell],
                    rect
                )

                # ----------------------------------------
                # DRAW KEY
                # ----------------------------------------

                if cell == KEY:

                    pygame.draw.circle(
                        self.screen,
                        (255, 240, 60),
                        (
                            c * TILE + TILE // 2,
                            r * TILE + TILE // 2
                        ),
                        10
                    )

                # ----------------------------------------
                # DRAW CHEST
                # ----------------------------------------

                elif cell == CHEST:

                    pygame.draw.rect(
                        self.screen,
                        (180, 120, 20),
                        rect.inflate(-12, -12),
                        border_radius=4
                    )

                # ----------------------------------------
                # TASK 1: DRAW TRAP
                # ----------------------------------------

                elif cell == TRAP:

                    pygame.draw.circle(
                        self.screen,
                        (120, 30, 30),
                        (
                            c * TILE + TILE // 2,
                            r * TILE + TILE // 2
                        ),
                        12
                    )

        # ------------------------------------------------
        # TASK 2: DRAW GUARD
        # ------------------------------------------------

        if self.guard:

            self.guard.draw(
                self.screen
            )

        # ------------------------------------------------
        # DRAW PLAYER
        # ------------------------------------------------

        self.player.draw(
            self.screen
        )

        # ------------------------------------------------
        # HUD
        # ------------------------------------------------

        hud = pygame.Rect(
            0,
            ROWS * TILE,
            WIDTH,
            50
        )

        pygame.draw.rect(
            self.screen,
            (20, 20, 35),
            hud
        )

        st = self.font.render(
            self.status + "  |  R=Restart",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            st,
            (
                8,
                ROWS * TILE + 13
            )
        )

        # ------------------------------------------------
        # WIN SCREEN
        # ------------------------------------------------

        if self.won:

            overlay = pygame.Surface(
                (WIDTH, ROWS * TILE),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 140)
            )

            self.screen.blit(
                overlay,
                (0, 0)
            )

            msg = self.big_font.render(
                "TREASURE FOUND!",
                True,
                (220, 180, 30)
            )

            sub = self.font.render(
                "Press R to Play Again",
                True,
                (180, 180, 180)
            )

            self.screen.blit(
                msg,
                (
                    WIDTH // 2
                    - msg.get_width() // 2,
                    ROWS * TILE // 2 - 30
                )
            )

            self.screen.blit(
                sub,
                (
                    WIDTH // 2
                    - sub.get_width() // 2,
                    ROWS * TILE // 2 + 20
                )
            )

        pygame.display.flip()

    def run(self):

        running = True

        while running:

            running = self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":

    engine = GameEngine()
    engine.run()