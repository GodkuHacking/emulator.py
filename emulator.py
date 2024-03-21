# -*- coding: utf-8 -*-
# emulator.py
# made by mindsetpro

from flask import Flask, render_template, send_file, request, redirect, url_for
import os
import pygame
from pygame.locals import *

class Emulator:
    def __init__(self, roms_dir='roms', static_folder='static', template_folder='templates'):
        self.app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
        self.roms_dir = roms_dir
        self.screen = None
        self.clock = pygame.time.Clock()
        self.running = False
        self.current_speed = 1  # Default speed

        # Define routes
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/play/<path:rom_path>', 'play', self.play)
        self.app.add_url_rule('/upload_rom', 'upload_rom', self.upload_rom, methods=['GET', 'POST'])
        self.app.add_url_rule('/change_speed/<int:speed>', 'change_speed', self.change_speed)

    def index(self):
        rom_files = os.listdir(self.roms_dir)
        return render_template('index.html', rom_files=rom_files)

    def play(self, rom_path):
        rom_file = os.path.join(self.roms_dir, rom_path)
        if os.path.exists(rom_file):
            pygame.init()
            pygame.display.set_caption("Emulator.py | made by mindsetpro")
            self.screen = pygame.display.set_mode((240, 160))
            self.running = True

            try:
                # Load and run the ROM
                game_rom = pygame.image.load(rom_file)
                self.screen.blit(game_rom, (0, 0))
                pygame.display.flip()

                while self.running:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            self.running = False
                            pygame.quit()
                            return ''
                    self.clock.tick(60 * self.current_speed)  # Adjust speed
            except pygame.error as e:
                self.running = False
                pygame.quit()
                return str(e)

        return 'ROM not found'

    def upload_rom(self):
        if request.method == 'POST':
            uploaded_file = request.files['rom']
            if uploaded_file.filename != '':
                rom_path = os.path.join(self.roms_dir, uploaded_file.filename)
                uploaded_file.save(rom_path)
                return redirect(url_for('index'))
        return render_template('upload_rom.html')

    def change_speed(self, speed):
        if speed in [1, 5, 10]:
            self.current_speed = speed
        return redirect(url_for('index'))

    def run(self, host='127.0.0.1', port=5000):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    emulator = Emulator()
    emulator.run()
