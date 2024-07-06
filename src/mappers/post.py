from src.models.post import Post
from src.schemas.post import PostDto


class PostMapper:
    @staticmethod
    def post_to_post_dto(post: Post) -> PostDto:
        return PostDto(
            content=post.content,
            id=str(post.id),
            title=post.title,
        )
