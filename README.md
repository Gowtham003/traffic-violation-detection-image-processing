Traffic Signal Violation Detection using Image Processing

• We design and implement a vehicular traffic violation detection system for cars. Our system proposes a algorithm using image processing techniques which can detect violations taking place on the traffic signal.
• By using high quality videos of traffic signal, we can detect each and every violating cars during the red signal and the license number of the vehicles can be identified using Plate Recognizer API. We can also identify the owner of the car/bus from the vehicle database and send an alert mail to them.
• The violation data will be helpful for the traffic department to make penalty for the violators and to reduce such kind of violations and traffics.
• Experimental results demonstrate that our system can discover almost all the violations from the traffic monitoring stream in real-time. Good scalability on multiple threads is also shown in the experimental results.

Input

– Date and time of the video
– Time when the red signal starts in the video
– Duration of red, yellow and green signal
– Position of stop line (Near/Far/Medium)
- Traffic Signal Video (720px)
- The vehicle data should be placed in "static_files" folder

Output

- Alert mail with image, date-time, licence number, place and other details of violation will be sent to the linked mail ids.
- Download Violated Data containing all the details of violated vehicles.

FRAMEWORK: Django, FRONT END: JS, HTML & CSS, BACK END: Python, OpenCV.

-Replace your Mail-ID and password for sending mails, and enable less secured app access for your account.
-Use your own Plate Recognizer API Token at https://api.platerecognizer.com to get 2500 free API calls per month.