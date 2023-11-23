from typing import Literal

set_ = "$set"
in_ = '$in'
push = '$push'
pull = '$pull'
add_to_set = '$addToSet'

MongoOperator = Literal[
    "$set",
    '$in',
    '$push',
    '$pull',
    '$addToSet'
]
