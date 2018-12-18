import sys
sys.path.append(".")

import entities

factory = entities.EntityFactory()
factory.add_class("tree")

e = factory.create("tree")

print(e.physics)
