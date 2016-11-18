$(document).ready(function(){
    var $product_in_car =$('#in_car');
    $('.add_car').click(function(e){
        e.preventDefault();

        var $tr= $(this).parents('tr');
        var $product_pk = $tr.attr('product-pk');
        var $product_name = $tr.find('.product_name').text();

        $.post('/car-add-product/',{'product_pk':$product_pk},function(response){
            if(response.success){
                $product_in_car.append(`<li product-pk="${$product_pk}">${$product_name}</li>`);
                $tr.addClass('info');
                $(this).attr('disabled',true);
            }else{
                alert(response.message);
            }
        })
    });

    $('.remove_product').click(function(e){
        e.preventDefault();
        var $tr= $(this).parents('tr');
        var $product_pk = $tr.attr('product-pk');
        $.post('/car-remove-product/',{'product_pk':$product_pk},function(response){
            if(response.success){
                $tr.fadeOut();
//                $tr.remove();
            }else{
                alert(response.message);
            }
        })
    });

    $product_in_car.find('li').each(function(){
        var product_pk = $(this).attr('product-pk');
        $tr = $('.products').find('[product-pk='+product_pk+']')
        $tr.find('.add_car').attr('disabled',true);
        $tr.addClass('info');
    });
});