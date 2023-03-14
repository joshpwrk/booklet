## Websocket

The websocket server is meant to be:
- tested locally
- deployed via AWS Elastic Beanstalk with AWS Elasticache acting as the redis server

### Beanstalk Environment

- Using ALB as socket.io relies on TCP (use ELB if switching to pure websocket)
- For horizontal scaling of the server, we must enable "sticky" sessions. This is done via the `.ebextensions/enable-websocket.config` file

### Inspiration

- https://aws.amazon.com/blogs/database/how-to-build-a-chat-application-with-amazon-elasticache-for-redis/
- https://binyamin.medium.com/node-websockets-with-aws-elastic-beanstalk-elastic-load-balancer-elb-or-application-load-6a693b21415a