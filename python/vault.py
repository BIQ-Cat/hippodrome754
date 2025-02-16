import pygame as pg


class MainDoor(pg.sprite.Sprite):
    def __init__(self, vault_images: tuple, *groups):
        super().__init__(*groups)

        self.vault_images = vault_images

        self.image = vault_images[0]

        self.rect = self.image.get_rect()
        self.rect.x = -91
        self.rect.y = 0

        self.frame_index = 0
        self.frame_count = len(vault_images)

    def get_x(self):
        return self.rect.x

    def get_frame_index(self):
        return self.frame_index
    
    def get_frame_count(self):
        return self.frame_count

    def set_image(self, i: int):
        self.frame_index = i
        self.image = self.vault_images[i]

    def move(self, x: int):
        self.rect = self.rect.move(x, 0)

    def set_x(self, x: int):
        self.rect.x = x


class SecondaryDoor(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        self.image = pg.image.load('../img/vaults/vault_half2.png')

        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 0

    def get_x(self):
        return self.rect.x

    def move(self, x: int):
        self.rect = self.rect.move(x, 0)

    def set_x(self, x: int):
        self.rect.x = x


class Vault:
    def __init__(self, screen):
        self.screen = screen
        
        self.door_group = pg.sprite.Group()
        self.secondary_door = SecondaryDoor(self.door_group)
        self.main_door = MainDoor((
            pg.image.load('../img/vaults/vault_half1.png'),
            pg.image.load('../img/vaults/vault.png'),
            pg.image.load('../img/vaults/vault1.png'),
            pg.image.load('../img/vaults/vault2.png'),
            pg.image.load('../img/vaults/vault3.png'),
            pg.image.load('../img/vaults/vault4.png'),
            pg.image.load('../img/vaults/vault5.png'),
            pg.image.load('../img/vaults/vault6.png'),
            pg.image.load('../img/vaults/vault7.png')), self.door_group)

        # self.is_opening_sound_played = False
        # self.is_open_sound_played = False

        self.is_process = False
        self.is_opening = False
        self.is_moving = False

    def get_vault_process(self):
        return self.is_process

    def open_vault(self):
        pg.mixer.music.load('../sounds/vault_process.mp3')
        pg.mixer.music.play()

        self.is_process = True
        self.is_opening = True
        self.is_moving = False

        self.main_door.set_x(1)
        self.secondary_door.set_x(91)

        self.main_door.set_image(self.main_door.get_frame_count() - 1)

        self.action_tick_start = pg.time.get_ticks()

    def close_vault(self):
        pg.mixer.music.load('../sounds/vault_process.mp3')
        pg.mixer.music.play()

        self.is_process = True
        self.is_opening = False
        self.is_moving = True

        self.main_door.set_x(-91)
        self.secondary_door.set_x(800)

        self.main_door.set_image(0)

    def update(self):
        self.door_group.draw(self.screen)

        if self.is_process:
            if self.is_opening:
                if self.is_moving:
                    if self.main_door.get_x() > -91:
                        self.main_door.move(-60)

                    if self.secondary_door.get_x() < 800:
                        self.secondary_door.move(180)

                    if self.main_door.get_x() <= -91 and self.secondary_door.get_x() >= 800:
                        self.is_process = False

                else:
                    frame_index = (pg.time.get_ticks() - self.action_tick_start) // 60

                    if frame_index != self.main_door.get_frame_index():
                        if frame_index >= self.main_door.get_frame_count():
                            pg.mixer.music.load('../sounds/vault_opened.mp3')
                            pg.mixer.music.play()

                            self.is_moving = True

                            self.main_door.set_image(0)

                        else:
                            self.main_door.set_image(frame_index)

            else:
                if self.is_moving:
                    if self.main_door.get_x() < 0:
                        self.main_door.move(60)

                    if self.secondary_door.get_x() > 91:
                        self.secondary_door.move(-180)

                    if self.main_door.get_x() >= 0 and self.secondary_door.get_x() <= 91:
                        self.is_moving = False

                        self.main_door.set_x(0)

                        self.action_tick_start = pg.time.get_ticks()

                else:
                    frame_index = (pg.time.get_ticks() - self.action_tick_start) // 60

                    if frame_index != self.main_door.get_frame_index():
                        if frame_index >= self.main_door.get_frame_count():
                            self.is_process = False

                        else:
                            self.main_door.set_image(self.main_door.get_frame_count() - frame_index)
    