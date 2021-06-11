This is UpdateTask Python Microservice

It contains a dockerfile which is used to create a docker image that is used in

containerDefinition part of ECS TaskDefinition for updatetask ECS service task

This is a frontend facing microservice with which end users communicate

Therefore it is hosted on an ECS Container EC2 Instance inside an ECS cluster residing in a public subnet

behind a public ALB , This microservice communicates with the backend dbtask microservice via private ALB to update records from the SQLITE database that the end users pass to

this microservice as a path parameter. This path parameter is primary id of the existing record
