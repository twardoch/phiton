from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from database import get_db_connection, User, Post

app = Flask(__name__)


@app.route("/api/users", methods=["GET"])
def get_users():
    """Get all users or filter by query parameters."""
    try:
        # Get query parameters
        active_only = request.args.get("active", "").lower() == "true"
        limit = request.args.get("limit", 100, type=int)

        # Get database connection
        db = get_db_connection()

        # Build query
        query = db.query(User)
        if active_only:
            query = query.filter(User.is_active == True)

        # Execute query with limit
        users = query.limit(limit).all()

        # Format response
        result = []
        for user in users:
            result.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active,
                    "post_count": len(user.posts),
                }
            )

        return jsonify({"users": result})

    except Exception as e:
        app.logger.error(f"Error fetching users: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by ID."""
    try:
        db = get_db_connection()
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get user's posts
        posts = []
        for post in user.posts:
            posts.append(
                {
                    "id": post.id,
                    "title": post.title,
                    "created_at": post.created_at.isoformat(),
                }
            )

        # Format response
        result = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "posts": posts,
        }

        return jsonify(result)

    except Exception as e:
        app.logger.error(f"Error fetching user {user_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
