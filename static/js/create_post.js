// static/js/create_post.js
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('createPostModal');
    const createBtn = document.querySelector('a[href*="create_post"]');
    const closeBtn = document.querySelector('.close');
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    const form = document.getElementById('createPostForm');

    createBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.style.display = "block";
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = "none";
        form.reset();
        imagePreview.style.backgroundImage = '';
    });

    window.addEventListener('click', function(e) {
        if (e.target == modal) {
            modal.style.display = "none";
            form.reset();
            imagePreview.style.backgroundImage = '';
        }
    });

    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.style.backgroundImage = `url(${e.target.result})`;
            }
            reader.readAsDataURL(file);
        }
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        try {
            const response = await fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                modal.style.display = "none";
                form.reset();
                imagePreview.style.backgroundImage = '';
                window.location.reload();
            } else {
                alert(data.error || 'Something went wrong');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});