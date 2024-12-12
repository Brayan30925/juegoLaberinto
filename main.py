import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 40  # Tamaño de los bloques del laberinto
ROWS = HEIGHT // BLOCK_SIZE
COLS = WIDTH // BLOCK_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Laberinto")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Fuente
font = pygame.font.Font(None, 74)
font2 = pygame.font.Font(None, 40)

# Posición inicial del jugador
player_x, player_y = BLOCK_SIZE, BLOCK_SIZE

# Meta final
goal_x, goal_y = (COLS - 2) * BLOCK_SIZE, (ROWS - 2) * BLOCK_SIZE

# Enemigos
enemies = [(BLOCK_SIZE * 4, BLOCK_SIZE * 3), (BLOCK_SIZE * 7, BLOCK_SIZE * 5)]

# Laberinto generado manualmente
maze = [
    [1 if x == 0 or y == 0 or x == COLS - 1 or y == ROWS - 1 else 0 for x in range(COLS)]
    for y in range(ROWS)
]

# Añadir obstáculos al laberinto
for _ in range((ROWS * COLS) // 5):
    x = random.randint(1, COLS - 2)
    y = random.randint(1, ROWS - 2)
    maze[y][x] = 1

# Reloj para controlar FPS
clock = pygame.time.Clock()


def draw_maze(maze):
    """Dibuja el laberinto en la pantalla."""
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            color = WHITE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def move_player(keys, player_x, player_y):
    """Mueve al jugador si no hay colisión con una pared."""
    new_x, new_y = player_x, player_y
    if keys[pygame.K_UP]:
        new_y -= BLOCK_SIZE
    if keys[pygame.K_DOWN]:
        new_y += BLOCK_SIZE
    if keys[pygame.K_LEFT]:
        new_x -= BLOCK_SIZE
    if keys[pygame.K_RIGHT]:
        new_x += BLOCK_SIZE

    # Verificar colisiones con el laberinto
    grid_x, grid_y = new_x // BLOCK_SIZE, new_y // BLOCK_SIZE
    if maze[grid_y][grid_x] == 0:  # Si es camino libre
        return new_x, new_y

    return player_x, player_y


def move_enemies():
    """Mueve a los enemigos automáticamente por el laberinto."""
    new_positions = []
    for x, y in enemies:
        direction = random.choice([(0, -BLOCK_SIZE), (0, BLOCK_SIZE), (-BLOCK_SIZE, 0), (BLOCK_SIZE, 0)])
        new_x, new_y = x + direction[0], y + direction[1]
        grid_x, grid_y = new_x // BLOCK_SIZE, new_y // BLOCK_SIZE

        # Solo mover si no colisionan con una pared
        if maze[grid_y][grid_x] == 0:
            new_positions.append((new_x, new_y))
        else:
            new_positions.append((x, y))

    return new_positions


def check_collision(player_x, player_y):
    """Verifica si el jugador colisiona con un enemigo."""
    for enemy_x, enemy_y in enemies:
        if player_x == enemy_x and player_y == enemy_y:
            return True
    return False


def show_message(message, color):
    """Muestra un mensaje central en la pantalla."""
    screen.fill(BLACK)
    text = font.render(message, True, color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    retry_text = font2.render("Presiona R para reiniciar o Q para salir", True, WHITE)
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()

    wait_for_retry()


def wait_for_retry():
    """Espera la entrada del jugador para reiniciar o salir."""
    global player_x, player_y, enemies
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    # Reiniciar posiciones y enemigos
                    player_x, player_y = BLOCK_SIZE, BLOCK_SIZE
                    enemies[:] = [(BLOCK_SIZE * 4, BLOCK_SIZE * 3), (BLOCK_SIZE * 7, BLOCK_SIZE * 5)]
                    main_game()
                elif event.key == pygame.K_q:  # Salir
                    pygame.quit()
                    sys.exit()


def main_menu():
    """Pantalla principal del menú."""
    while True:
        screen.fill(GRAY)
        title = font.render("Juego de Laberinto", True, BLUE)
        play_button = font.render("Iniciar Juego", True, GREEN)
        quit_button = font.render("Salir", True, RED)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(play_button, (WIDTH // 2 - play_button.get_width() // 2, 250))
        screen.blit(quit_button, (WIDTH // 2 - quit_button.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 250 <= mouse_y <= 250 + play_button.get_height():
                    main_game()  # Ir al juego
                elif 350 <= mouse_y <= 350 + quit_button.get_height():
                    pygame.quit()
                    sys.exit()


def main_game():
    """Función principal del juego."""
    global player_x, player_y, enemies
    game_running = True

    while game_running:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        player_x, player_y = move_player(keys, player_x, player_y)

        # Mover enemigos
        enemies = move_enemies()

        # Verificar colisiones
        if check_collision(player_x, player_y):
            show_message("¡Perdiste!", RED)

        # Verificar si el jugador alcanza la meta
        if player_x == goal_x and player_y == goal_y:
            show_message("¡Ganaste!", GREEN)

        # Dibujar pantalla
        screen.fill(BLACK)
        draw_maze(maze)
        pygame.draw.rect(screen, BLUE, (player_x, player_y, BLOCK_SIZE, BLOCK_SIZE))  # Jugador
        pygame.draw.rect(screen, GREEN, (goal_x, goal_y, BLOCK_SIZE, BLOCK_SIZE))  # Meta
        for enemy_x, enemy_y in enemies:
            pygame.draw.rect(screen, RED, (enemy_x, enemy_y, BLOCK_SIZE, BLOCK_SIZE))  # Enemigos

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(10)

    main_menu()


if __name__ == "__main__":
    main_menu()
