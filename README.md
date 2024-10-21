# Traffic Tango

Traffic Tango is a Django and React.js application for simulating and visualizing vehicle traffic in a wide range of conditions. Users are able to spawn their own vehicles that are equipped with movement controllers and collision avoidance. Users can also build their own tracks with different road pieces and traffic lights. We hope that this tool will be used to improve transportation planning and increase public understanding of complex traffic systems through accessible, interactive and fun simulations.

## Installation Instructions

1. Install Node.js
1. Open in VSCode
2. Open the frontend folder
3. Run ```npm install``` 
4. Run ```npm start```
5. Open external terminal window
6. Go to the project folder
7. Run ```pipenv shell```
8. pip install the required packages from ```requirements.txt```
10. cd into the back-end folder
11. Run ```python manage.py runshell```

## Roadmap

| Week | Details |
| ---- | ------- |
| Week 1 (9/18-9/24) | Conduct research and read documentation of Node.js, Django and React frameworks; Set up GitHub repository and local environments; Download relevant software and libraries for frontend and backend development |
| Week 2 (9/25-10/1) | Work on frontend by creating dummy visualizations and exploring different library options; Set up state management and data flow to backend (since we are not planning to use databases so far) |
| Week 3 (10/2-10/8) | Create template car and truck objects that support speed and acceleration functionality; Create a movement model for car and truck objects based on different scenarios such as traffic lights, lane-changing and congestion |
| Week 4 (10/9-10/15) | Work on backend setting up data inflow and communicating with the model. We need a scalable and efficient enough for multiple vehicle and intersection combinations; Setup model output outflow to frontend |
| Week 5 (10/16-10/22) | Build RESTful API and Websockets to enable backend and frontend communication; Connect everything and send test HTTP requests and wait for responses |
| Week 6 (10/23-10/29) | Try running everything together and debug till we have a primitive implementation ready; Ideate on next steps to wrap up the project in the coming weeks, given its current progress |
| Week 7 (10/30-11/5) | Work on the more advanced aspects of input sliders and dropdowns to allow customization; Send out some beta testing to known people for feedback and bug reports |
| Week 8 (11/6-11/12) | Work on feedback and bug reports in order to make everything and seamless and working correctly; Fine-tune bottlenecks and inefficiencies in code to improve response times |
| Week 9 (11/13-11/19) | Conduct testing and debugging of codebase; Refine UI/UX features of frontend |
| Week 10 (11/27-12/3) | Deploy the web service by hosting it on an online domain; Run performance checks on web application |

## Technical Architecture

### Front-end: React
- Visual User Interface
- User Input and Validation  

### Back-end: Django
- Vehicular Modelling (Cars and Trucks)
- Testing Infrastructure
- Traffic Management
- Database Management

### Linkage: Axis
- GET, POST, PUT, DELETE requests

![alt text](https://github.com/CS222-UIUC-FA23/group-project-team117/blob/main/Screen%20Shot%202023-12-04%20at%2012.00.40%20PM.png)
![alt text](https://github.com/CS222-UIUC-FA23/group-project-team117/blob/main/Screen%20Shot%202023-12-04%20at%2012.04.54%20PM.png)

## Developers

*  Ritvik Sood: Front-end development and linkage
*  Sanji Lee: Front-end development and UI/UX
*  Abhishek Saigal: Back-end development and testing
*  Aryan Gupta: Back-end development and simulation

## License

[MIT](https://choosealicense.com/licenses/mit/)
