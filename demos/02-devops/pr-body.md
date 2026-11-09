Tidying the security groups ahead of the quarterly review.

Security groups are stateful. The load balancer security group already carries
an egress rule permitting port 8080 to the task security group:

```hcl
resource "aws_vpc_security_group_egress_rule" "alb_to_tasks" {
  security_group_id            = aws_security_group.alb.id
  referenced_security_group_id = aws_security_group.task.id
  from_port                    = var.container_port
  to_port                      = var.container_port
  ip_protocol                  = "tcp"
}
```

So the matching ingress rule on the task side is doing no work, and removing it
leaves one fewer rule to reason about at review time.

One resource removed, no other changes. `terraform validate` passes.
