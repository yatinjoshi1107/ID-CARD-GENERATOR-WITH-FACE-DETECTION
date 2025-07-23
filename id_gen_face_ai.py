from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageDraw, ImageFont
import random
import os
import datetime
import qrcode
import cv2
import sys
import numpy as np

# Try to import face_recognition, but make it optional
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("Face recognition module not available. Will skip face detection.")

# Constants for ID card image
ID_PHOTO_WIDTH = 300
ID_PHOTO_HEIGHT = 300

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(799, 594)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        Form.setFont(font)
        Form.setStyleSheet("QWidget{ background:rgb(85, 170, 255); }")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 30, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(self.capture)
        self.pushButton.setStyleSheet("QPushButton{ border:3px solid black; border-radius:15px; background:blue; color:white; } QPushButton:hover{ border:1px solid gray; border-radius:15px; background:black; color:white; }")
        self.pushButton.setObjectName("pushButton")

        # Add a button to select an image file instead of using webcam
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(620, 30, 151, 41))
        self.pushButton_3.setFont(font)
        self.pushButton_3.clicked.connect(self.select_image)
        self.pushButton_3.setStyleSheet("QPushButton{ border:3px solid black; border-radius:15px; background:blue; color:white; } QPushButton:hover{ border:1px solid gray; border-radius:15px; background:black; color:white; }")
        self.pushButton_3.setObjectName("pushButton_3")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 30, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 201, 21))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(70, 230, 181, 21))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(70, 310, 161, 21))
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(70, 390, 171, 21))
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(70, 490, 231, 21))
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(360, 140, 381, 31))
        self.lineEdit.setStyleSheet("QLineEdit{ background:white; }")
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(360, 220, 381, 31))
        self.lineEdit_2.setStyleSheet("QLineEdit{ background:white; }")
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(360, 300, 381, 31))
        self.lineEdit_3.setStyleSheet("QLineEdit{ background:white; }")
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(360, 390, 381, 31))
        self.lineEdit_4.setStyleSheet("QLineEdit{ background:white; }")
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(360, 480, 381, 31))
        self.lineEdit_5.setStyleSheet("QLineEdit{ background:white; }")
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 540, 271, 41))
        self.pushButton_2.setFont(font)
        self.pushButton_2.clicked.connect(self.generate_idcard)
        self.pushButton_2.setStyleSheet("QPushButton{ border:3px solid black; border-radius:15px; background:blue; color:white; } QPushButton:hover{ border:1px solid gray; border-radius:15px; background:black; color:white; }")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        # Initialize form variable for later use
        self.Form = Form

    def resize_image(self, img):
        """Resize image to the required size for ID card"""
        # Convert to PIL Image if it's an OpenCV image
        if isinstance(img, np.ndarray):
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            img_pil = img
            
        # Resize maintaining aspect ratio
        img_pil.thumbnail((ID_PHOTO_WIDTH, ID_PHOTO_HEIGHT), Image.Resampling.LANCZOS)
        
        # Create a white background image
        background = Image.new('RGB', (ID_PHOTO_WIDTH, ID_PHOTO_HEIGHT), (255, 255, 255))
        
        # Calculate position to paste the resized image (center it)
        offset = ((ID_PHOTO_WIDTH - img_pil.width) // 2, 
                 (ID_PHOTO_HEIGHT - img_pil.height) // 2)
        
        # Paste the resized image onto the background
        background.paste(img_pil, offset)
        
        # If input was OpenCV image, convert back to OpenCV format
        if isinstance(img, np.ndarray):
            return cv2.cvtColor(np.array(background), cv2.COLOR_RGB2BGR)
        
        return background

    def select_image(self):
        """Allow user to select an image file instead of using webcam"""
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self.Form, 
            "Select Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            try:
                # Open the image
                img = cv2.imread(file_path)
                
                # Resize image to required dimensions
                img_resized = self.resize_image(img)
                
                # Save the resized image
                cv2.imwrite('person.jpg', img_resized)
                
                # Check face if face_recognition is available
                if FACE_RECOGNITION_AVAILABLE:
                    self.check_faces('person.jpg')
                else:
                    QtWidgets.QMessageBox.information(None, "Image Selected", "Image selected and resized successfully!")
                    
                # Show the resized image
                cv2.imshow('Selected and Resized Image', img_resized)
                cv2.waitKey(2000)  # Show for 2 seconds
                cv2.destroyAllWindows()
                
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Error processing image: {str(e)}")

    def capture(self):
        try:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                QtWidgets.QMessageBox.critical(None, "Error", "Could not access webcam. Try using the 'Select Image' button instead.")
                return
            
            # Create a window with capture button
            cv2.namedWindow('Webcam Capture')
            
            capture_clicked = False
            image_captured = None
            
            while not capture_clicked:
                return_value, frame = camera.read()
                if not return_value:
                    QtWidgets.QMessageBox.critical(None, "Error", "Failed to capture image from webcam.")
                    break
                    
                # Flip the image horizontally
                frame = cv2.flip(frame, 1)
                
                # Create a copy of the frame to draw the button on
                display_frame = frame.copy()
                
                # Draw a capture button on the frame
                button_width, button_height = 200, 50
                button_x = (frame.shape[1] - button_width) // 2
                button_y = frame.shape[0] - button_height - 20
                cv2.rectangle(display_frame, (button_x, button_y), 
                              (button_x + button_width, button_y + button_height), 
                              (0, 255, 0), -1)
                cv2.putText(display_frame, "Capture", (button_x + 50, button_y + 35), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                
                # Show the frame with the button
                cv2.imshow('Webcam Capture', display_frame)
                
                # Check for key press or mouse click
                key = cv2.waitKey(1)
                if key == 27:  # ESC key to exit
                    break
                elif key == 13:  # Enter key to capture
                    image_captured = frame.copy()
                    capture_clicked = True
                
                # Check for mouse events to detect button clicks
                def on_mouse_click(event, x, y, flags, param):
                    nonlocal capture_clicked, image_captured
                    if event == cv2.EVENT_LBUTTONDOWN:
                        # Check if click is within button area
                        if (button_x <= x <= button_x + button_width and 
                            button_y <= y <= button_y + button_height):
                            image_captured = frame.copy()
                            capture_clicked = True
                
                cv2.setMouseCallback('Webcam Capture', on_mouse_click)
                
            camera.release()
            cv2.destroyAllWindows()
            
            if image_captured is not None:
                # Resize image to required dimensions
                img_resized = self.resize_image(image_captured)
                
                # Save the resized image
                cv2.imwrite('person.jpg', img_resized)
                
                # Show the resized image
                cv2.imshow('Captured and Resized Image', img_resized)
                cv2.waitKey(2000)  # Show for 2 seconds
                cv2.destroyAllWindows()
                
                # If face_recognition is available, use it to check for faces
                if FACE_RECOGNITION_AVAILABLE:
                    self.check_faces('person.jpg')
                else:
                    QtWidgets.QMessageBox.information(None, "Image Captured", "Image captured and resized successfully!")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Error capturing image: {str(e)}")

    def check_faces(self, image_path):
        """Check for faces in the image if face_recognition is available"""
        if not FACE_RECOGNITION_AVAILABLE:
            return
            
        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)

            if len(face_locations) == 0:
                QtWidgets.QMessageBox.critical(None, "Error", "No face detected. Try again.")
                return False
            elif len(face_locations) > 1:
                QtWidgets.QMessageBox.critical(None, "Error", "Multiple faces detected. Try again.")
                return False
            else:
                QtWidgets.QMessageBox.information(None, "Success", "Face detected successfully!")
                return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Error in face detection: {str(e)}")
            return False

    def generate_idcard(self):
        if not os.path.exists("person.jpg"):
            choice = QtWidgets.QMessageBox.question(
                None, 
                "No Image", 
                "No image has been captured or selected. Do you want to continue without an image?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if choice == QtWidgets.QMessageBox.No:
                return
                
        # Check if required fields are filled
        if not self.lineEdit.text() or not self.lineEdit_2.text():
            QtWidgets.QMessageBox.warning(None, "Missing Information", "Company name and Full name are required.")
            return
                
        image = Image.new('RGB', (1000, 900), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', size=45)
        date = datetime.datetime.now()

        company = self.lineEdit.text()
        name = self.lineEdit_2.text()
        gender = self.lineEdit_3.text()
        address = self.lineEdit_4.text()
        phone = self.lineEdit_5.text()
        id_no = random.randint(1000000, 9000000)

        draw.text((50, 50), company, fill='black', font=ImageFont.truetype('arial.ttf', size=80))
        draw.text((50, 250), name, fill='black', font=font)
        draw.text((50, 350), f"ID {id_no}", fill='red', font=ImageFont.truetype('arial.ttf', size=60))
        draw.text((50, 550), gender, fill='black', font=font)
        draw.text((50, 650), phone, fill='black', font=font)
        draw.text((50, 750), address, fill='black', font=font)

        image.save(f"{name}.png")

        # Try to add the photo if it exists
        try:
            card_image = Image.open(f"{name}.png")
            if os.path.exists("person.jpg"):
                person_image = Image.open("person.jpg")
                card_image.paste(person_image, (600, 75))
                card_image.save("card.jpg")
            else:
                card_image.save("card.jpg")
        except Exception as e:
            print(f"Error adding photo: {e}")
            image.save("card.jpg")

        # Generate QR code
        try:
            qr = qrcode.make(f"{company}{id_no}")
            qr.save(f"{id_no}.bmp")

            qr_img = Image.open(f"{id_no}.bmp")
            final_card = Image.open("card.jpg")
            final_card.paste(qr_img, (600, 400))
            final_card.save(f"{name}.png")
            
            # Open the generated ID card
            try:
                os.startfile(f"{name}.png")
            except:
                pass
                
            QtWidgets.QMessageBox.information(None, "Success", f"ID Card generated successfully as {name}.png")
        except Exception as e:
            print(f"Error generating QR code: {e}")
            QtWidgets.QMessageBox.warning(None, "Warning", f"Could not generate QR code: {e}")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ID Card Generator"))
        self.pushButton.setText(_translate("Form", "Capture Image"))
        self.pushButton_3.setText(_translate("Form", "Select Image"))
        self.label.setText(_translate("Form", "Get Your Image"))
        self.label_2.setText(_translate("Form", "Your Company Name"))
        self.label_3.setText(_translate("Form", "Your Full Name"))
        self.label_4.setText(_translate("Form", "Your Gender"))
        self.label_5.setText(_translate("Form", "Your Current Address"))
        self.label_6.setText(_translate("Form", "Your Active Phone Number"))
        self.pushButton_2.setText(_translate("Form", "Generate ID Card"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
