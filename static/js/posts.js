document.addEventListener('DOMContentLoaded', function() {
    // Like functionality
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            try {
                const response = await fetch(`/posts/${postId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                });
                const data = await response.json();
                if (data.success) {
                    this.classList.toggle('active');
                    // Update likes count
                    const likesCount = this.closest('.post').querySelector('.likes-count');
                    likesCount.textContent = `${data.likes_count} likes`;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
});