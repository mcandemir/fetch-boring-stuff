import time
from scripts.util import clear

# ======================================================================================================================
class FetchCubis:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.loggedin = "(Not Logged in)"

    # ------------------------------------------------------------------------------------------------------------------

    def start(self):
        self.main_menu()

    # ------------------------------------------------------------------------------------------------------------------
    def login(self):
        # Enter website
        print('Entering website..')
        self.driver.get(self.config['cubis']['login_url'])
        print('++Done.')

        time.sleep(2)

        # login
        print('Logging in..')
        username_box = self.driver.find_element_by_name(self.config['cubis']['username_box_%name%'])
        password_box = self.driver.find_element_by_name(self.config['cubis']['password_box_%name%'])
        login_button = self.driver.find_element_by_id(self.config['cubis']['login_button_%id%'])
        username_box.send_keys(self.config['cubis']['username'])
        password_box.send_keys(self.config['cubis']['password'])
        login_button.click()
        print('++Done.')

        if self.driver.current_url == self.config['cubis']['login_url']:
            print("\nWrong username or password\n")
            return

        print('Entering the OBS..')
        self.driver.get(self.config['cubis']['obs_url'])
        print('++Done.')

        self.loggedin = "(Logged in)"

    # ------------------------------------------------------------------------------------------------------------------

    def fetch_grades(self):
        # go to courses
        print('Entering the Courses..')
        self.driver.get(self.config['cubis']['courses_url'])
        print('++Done.')

        time.sleep(2)

        # fetch every course data
        courses = self.driver.find_elements_by_class_name(self.config['cubis']['course_data_%class%'])

        # iterate over all text and collect course data
        course_data = {}
        for i in courses[1:]:
            content = i.text

            # detect a course name and create a key
            if '-' in content:
                course_name = content[content.index('-') + 2:]
                course_data[course_name] = {}
                continue

            # add data to detected course
            # get AKTS
            if 'AKTS' in content:
                course_data[course_name]['akts'] = content[0]

            # fetch other data
            if 'Oran ' in content:
                # content = content.replace

                # check if any midterm exists
                if '40 Ödev' in content or '40 Ara Sınav' in content:
                    course_data[course_name]['is_midterm_exist'] = True
                    course_data[course_name]['midterm'] = content[content.index('\n40') + 3: content.index('\n60')]

                else:
                    course_data[course_name]['is_midterm_exist'] = False

                # check if any final exists
                if '60 Yıl' in content:
                    course_data[course_name]['is_final_exist'] = True
                    course_data[course_name]['final'] = content[content.index('\n60') + 3: content.index('\nB')]

                else:
                    course_data[course_name]['is_final_exist'] = False

                # average score
                course_data[course_name]['basari_notu'] = content[content.index('\nB') + 1:]

        for course, values in course_data.items():
            print(course)
            for key, value in values.items():
                print('\t\t', key, ':', value)
            print('\n')
        print(f'total of {len(course_data.keys())} courses\n')

        print('Returning to Welcome Page..')
        self.driver.get(self.config['cubis']['obs_url'])
        print('++Done.')
        input('Press enter to continue..\n')

    # ------------------------------------------------------------------------------------------------------------------

    def fetch_gpa(self):
        gpa = self.driver.find_element_by_id('ContentPlaceHolderOrtaAlan_ContentPlaceHolderIcerik_duyuru_lblOrtalama')
        input(f'GPA:{gpa.text}\nPress enter to continue..\n')

    # ------------------------------------------------------------------------------------------------------------------

    def logout(self):
        print('Logging out')
        logout_button = self.driver.find_element_by_xpath('//*[@id="kullanici_aciklama"]/div[3]/a')
        logout_button.click()
        print('++Done')

        self.loggedin = "(Not Logged in)"

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def main_menu(self):
        while True:
            print(self.loggedin)
            if self.loggedin == "(Logged in)":
                print('\n=======OBS Page======', self.loggedin)
                opt = input(f"=========================\n\n1-Get grades\n2-Get gpa\n3-Logout and leave Cubis\n\nopt: ")

                if opt == '1':
                    self.fetch_grades()

                elif opt == '2':
                    self.fetch_gpa()

                elif opt == '3':
                    self.logout()
                    break

            else:
                print('\n=======OBS Page======', self.loggedin)
                opt = input(f"=========================\n\n1-Login\n2-Leave Cubis\n\nopt: ")

                if opt == '1':
                    self.login()

                elif opt == '2':
                    break

            clear()

    # ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================