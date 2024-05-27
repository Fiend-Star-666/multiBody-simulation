import pygame


def handle_events(events, mode, additional_params=None):
    if mode == 'start_sim':
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    return True
    elif mode == 'runtime':
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    additional_params['pause'] = not additional_params['pause']
                if event.key == pygame.K_t:
                    additional_params['trail'] = not additional_params['trail']
    return False
