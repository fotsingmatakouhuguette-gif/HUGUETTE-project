Create button rectangles
        button_rects = []
        y = 180
        for i, opt in enumerate(options):
            button_rect = pygame.Rect(WIDTH//2 - 100, y, 200, 45)
            button_rects.append(button_rect)
            
            # Check if mouse is hovering over button
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = button_rect.collidepoint(mouse_pos)
            
            draw_button(opt, FONT_MED, YELLOW if is_hovering else WHITE, 
                       BOX_COLOR, button_rect.x, button_rect.y, button_rect.width, button_rect.height, False)
            y += 60

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(e.pos):
                        if i == 0:
                            play_game()
                        elif i == 1:
                            how_to_play_screen()
                        elif i == 2:
                            sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    pass
                if e.key == pygame.K_DOWN:
                    pass
                if e.key == pygame.K_RETURN:
                    pass

        pygame.display.update()
        clock.tick(60)

main_menu()c