function edit(id) {
    edit_text = document.getElementById(`edit-text${id}`);
    edit_button = document.getElementById(`edit-button${id}`);
    save_button = document.getElementById(`save-button${id}`);
    cancel_button = document.getElementById(`cancel-button${id}`);
    edit_view = document.getElementById(`edit-view${id}`);
    article_content = document.getElementById(`article-content${id}`);
    publish_button = document.getElementById(`publish-button${id}`);

    edit_view.style.display = 'block';
    edit_button.style.display = 'none';
    if(publish_button){
        publish_button.style.display = 'none';
    }
    article_content.style.display = 'none';

    cancel_button.addEventListener('click', () => {
        edit_view.style.display = 'none';
        edit_button.style.display = 'block';
        if(publish_button){
            publish_button.style.display = 'block';
        }
        article_content.style.display = 'block';
    });

    save_button.addEventListener('click', () => {
        fetch(`/edit/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: edit_text.value
            })
        });
        edit_view.style.display = 'none';
        article_content.style.display = 'block';
        edit_button.style.display = 'block';
        if(publish_button){
            publish_button.style.display = 'block';
        }
        
        document.getElementById(`article-content${id}`).innerHTML = edit_text.value;
    });
 
}
