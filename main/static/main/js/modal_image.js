$(document).ready(function(){
    $('.fire-modal').click(function(e){
        $('.bs-example-modal-lg .modal-content .image-preview').attr('src',($(e.target).attr('data-image')));
        $('.bs-example-modal-lg .modal-content .modal-title').text($(e.target).attr('data-title'));
    });
});