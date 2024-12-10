from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Flask Guide", "content": "Learn how to build APIs with Flask."},
    {"id": 4, "title": "API Design", "content": "Best practices for designing APIs."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Retrieve query parameters
    sort_field = request.args.get('sort', None)
    sort_direction = request.args.get('direction', 'asc').lower()

    # Validate sort parameters
    valid_sort_fields = ['title', 'content']
    valid_sort_directions = ['asc', 'desc']

    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field '{sort_field}'. Valid fields are 'title' or 'content'."}), 400

    if sort_direction not in valid_sort_directions:
        return jsonify({"error": f"Invalid sort direction '{sort_direction}'. Valid directions are 'asc' or 'desc'."}), 400

    # Sort posts if sort parameters are provided
    sorted_posts = POSTS[:]
    if sort_field:
        reverse = sort_direction == 'desc'
        sorted_posts.sort(
            key=lambda post: post[sort_field].lower() if isinstance(post[sort_field], str) else post[sort_field],
            reverse=reverse
        )

    return jsonify(sorted_posts)




@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if 'title' not in data or 'content' not in data:
        return jsonify({"error": "Both 'title' and 'content' are required."}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((post for post in POSTS if post['id'] == post_id), None)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((post for post in POSTS if post['id'] == post_id), None)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    data = request.get_json()

    # Update title and/or content if provided
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    # Filter posts based on the query parameters
    filtered_posts = [
        post for post in POSTS
        if (title_query in post['title'].lower() if title_query else True) and
           (content_query in post['content'].lower() if content_query else True)
    ]

    return jsonify(filtered_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
