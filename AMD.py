from settings import *

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)


def accept_cookies():
    try:
        cookies = driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        cookies.click()
    except:
        print("No cookies button found / Problem with the cookies")

def log_in():
    try:
        login = driver.find_element(By.XPATH, '//*[@id="navigation"]/div/nav/div[3]/ul/li[1]/a')
        login.click()
        time.sleep(0.1)
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        email.click()
        email.clear()
        email.send_keys("thomaslarosemasson@gmail.com")
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        password.clear()
        password.send_keys("7#@24&sv4MRzUe*fEeCK")
        password.send_keys(Keys.ENTER)
        
    except:
        print("No login button found / Problem with the login")


driver.get("https://freemusicarchive.org/music/charts/this-month")
time.sleep(0.3)
accept_cookies()
time.sleep(0.3)
log_in()
time.sleep(0.5)

musiques = driver.find_elements(By.CLASS_NAME, "play-item")
nb_downloads = 0
for i in range(len(musiques)):
    retries = 3
    while retries > 0:
        try:
            current_music = driver.find_elements(By.CLASS_NAME, "play-item")[i]
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", current_music)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(current_music)
            )
            current_music.click()
            download_arrow = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div[3]/div[2]/div[3]/div[{i+1}]/span[7]/a[1]"))
            )
            download_arrow.click()
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="downloadOverlay"]/div[2]/div[1]/div[2]/a'))
            )
            confirm_button.click()
            nb_downloads += 1
            time.sleep(0.3)
            break
            
        except (NoSuchElementException, StaleElementReferenceException) as e:
            retries -= 1
            time.sleep(0.3)
            if retries == 0:
                print(f"Échec sur la musique {i+1}")
                continue

#driver.quit()

#---------------------------------------------------------------------------------------

class Bouton():

    def __init__(self, x, y, width, height, type, color, color_text, image):
        self.clicked = False
        self.type = type
        if self.type == "colored":
            self.rect = pygame.draw.rect(SCREEN, color, (x, y, width, height))
            self.x, self.y = x, y
            self.width, self.height = width, height
            self.color = color
            self.color_text = color_text
        elif self.type == "image":
            self.image = pygame.transform.scale(image, (width, height))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def draw(self):
        reset_click = False
        mouse_cos = pygame.mouse.get_pos()
        if self.type == "colored":
            pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.width, self.height))
        elif self.type == "image":
            SCREEN.blit(self.image, self.rect)
        if self.rect.collidepoint(mouse_cos):
            """This part of the code handles all bugs with buttons (so when the user clicks it clicks one time and one time only) (scuffed ik)"""
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                reset_click = True
                self.clicked = False
        return reset_click


def draw_text(texte, font, couleur, x, y, centered = True):
    """small function used to draw text"""
    img = font.render(texte, True, couleur)
    if centered:
        text_width, text_height = font.size(texte)
    else:
        text_width, text_height = 0, 0
    SCREEN.blit(img, (x - text_width // 2, y - text_height // 2))

def save():
    pickle_out = open('data/data_main', 'wb')
    data[0] = clr_background
    data[1] = clr_text
    pickle.dump(data, pickle_out)
    pickle_out.close()

pickle_in = open(f'data/data_main', 'rb')
data = pickle.load(pickle_in)
clr_background = data[0]
clr_text = data[1]

bouton_black = Bouton(SCREEN_WIDTH - 40, 10, 30, 30, "colored", (0,0,0), CLR_WHITE, None)
bouton_red = Bouton(SCREEN_WIDTH - 40, 45, 30, 30, "colored", (202, 60, 102), CLR_WHITE, None)
bouton_green = Bouton(SCREEN_WIDTH - 40, 80, 30, 30, "colored", (149,212,175), CLR_WHITE, None)
bouton_yellow = Bouton(SCREEN_WIDTH - 40, 115, 30, 30, "colored", (235,212,169), CLR_BLACK, None)
bouton_white = Bouton(SCREEN_WIDTH - 75, 10, 30, 30, "colored", (243,243,243), CLR_BLACK, None)
bouton_brown = Bouton(SCREEN_WIDTH - 75, 45, 30, 30, "colored", (182, 115, 50), CLR_WHITE, None)
bouton_blue = Bouton(SCREEN_WIDTH - 75, 80, 30, 30, "colored", (87, 132, 186), CLR_WHITE, None)
bouton_pink = Bouton(SCREEN_WIDTH - 75, 115, 30, 30, "colored", (255, 122, 209), CLR_WHITE, None)
exit_img = pygame.image.load("sprites/img_bouton_exit.webp")
bouton_exit = Bouton(7, 7, 67, 37, "image", None, None, exit_img)

img_fleche = pygame.image.load("sprites/img_fleche.webp")
img_fleche_flip = pygame.transform.flip(img_fleche, True, False)
bouton_colors = Bouton(SCREEN_WIDTH - 27, 15, 23, 31, "image", None, None, img_fleche_flip)
bouton_colors_bis = Bouton(SCREEN_WIDTH - 107, 15, 23, 31, "image", None, None, img_fleche_flip)
boutons_colored = [bouton_black, bouton_green, bouton_yellow, bouton_white, bouton_red, bouton_brown, bouton_blue, bouton_pink]
menu_colors = False


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            run = False

    CLOCK.tick(60)
    SCREEN.fill(clr_background)
    draw_text(f"Nombre de musiques téléchargées: {nb_downloads}", FONT_LILITAONE_50, clr_text, SCREEN_WIDTH // 2 - 30, 45)
    draw_text("© TraZe 2025", FONT_LILITAONE_10, clr_text, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 5)
    
    if not menu_colors:
        if bouton_colors.draw():
            menu_colors = True
    else:
        pygame.draw.rect(SCREEN, (100,100,100), (SCREEN_WIDTH - 80, 5, 75, 145))
        for bouton in boutons_colored:
            if bouton.draw():
                clr_background = bouton.color
                clr_text = bouton.color_text
        if bouton_colors_bis.draw():
            menu_colors = False

    if bouton_exit.draw():
        run = False

    pygame.display.update()

pygame.quit()