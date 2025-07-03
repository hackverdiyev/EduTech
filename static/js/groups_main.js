function open_delete_div_main(k){
    var delete_div = document.querySelector('.delete_group_div'+k.toString());
    delete_div.style.display = "flex";
    delete_div.animate([{opacity:'0.0'}, {opacity:'1.0'}],
    {duration: 500, fill:'forwards'});
}

function close_delete_div_main(k){
    var delete_div = document.querySelector('.delete_group_div'+k.toString());
    delete_div.style.display = "none";
}

document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete_group');
    const cancelButtons = document.querySelectorAll('.cancel_deleting');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const groupId = this.dataset.groupId;
            open_delete_div_main(groupId);
        });
    });
    cancelButtons.forEach(button => {
        button.addEventListener('click', function () {
            const groupId = this.dataset.groupId;
            close_delete_div_main(groupId);
        });
    });
});