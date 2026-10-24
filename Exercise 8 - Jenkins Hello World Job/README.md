# Exercise 8 - Jenkins Hello World Job

This is the source repository for a Jenkins Freestyle job named
`HelloWorld`. The job checks out this folder and runs the build step below:

```bash
sh hello-world.sh
```

The successful console output must include:

```text
Hello, Jenkins!
Finished: SUCCESS
```

Create the job in Jenkins as a **Freestyle project**, configure Git source
control for this repository, add `sh hello-world.sh` under **Execute shell**,
save it, and select **Build Now**.

## Execution Evidence / Screenshots

![Exercise 8 screenshot 1](screenshots/exercise_8_1.png)
![Exercise 8 screenshot 2](screenshots/exercise_8_2.png)
![Exercise 8 screenshot 3](screenshots/exercise_8_3.png)
![Exercise 8 screenshot 4](screenshots/exercise_8_4.png)
![Exercise 8 screenshot 5](screenshots/exercise_8_5.png)
![Exercise 8 screenshot 6](screenshots/exercise_8_6.png)
