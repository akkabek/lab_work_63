document.addEventListener('DOMContentLoaded', () => {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    const csrftoken = csrfMeta ? csrfMeta.content : '';

    document.querySelectorAll('.js-like-btn').forEach((button) => {
        button.addEventListener('click', () => toggleLike(button, csrftoken));
    });
});

async function toggleLike(button, csrftoken) {
    const postId = button.dataset.postId;
    const isLiked = button.dataset.liked === 'true';
    const url = `/api/posts/${postId}/like/`;

    button.disabled = true;

    try {
        const response = await fetch(url, {
            method: isLiked ? 'DELETE' : 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            console.error('Не удалось изменить лайк:', response.status);
            return;
        }

        const data = await response.json();
        applyLikeState(postId, data.liked, data.likes_count);
    } catch (error) {
        console.error('Ошибка сети при попытке лайкнуть публикацию:', error);
    } finally {
        button.disabled = false;
    }
}

function applyLikeState(postId, liked, likesCount) {
    document.querySelectorAll(`.js-like-btn[data-post-id="${postId}"]`).forEach((button) => {
        button.dataset.liked = liked ? 'true' : 'false';
        button.textContent = liked ? '❤️' : '🤍';
        button.title = liked ? 'Вы уже лайкнули' : 'Нравится';
    });

    document.querySelectorAll(`.js-likes-count[data-post-id="${postId}"]`).forEach((el) => {
        el.textContent = `${likesCount} отметок «Нравится»`;
    });
}
