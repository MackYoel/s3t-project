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

    $product_in_car.find('li').each(function(){
        var product_pk = $(this).attr('product-pk');
        $tr = $('.products').find('[product-pk='+product_pk+']')
        $tr.find('.add_car').attr('disabled',true);
        $tr.addClass('info');
    });


    // USED IN UPDATE ORDER
    $('.remove_product').click(function(e){
        e.preventDefault();
        var $tr= $(this).parents('tr');
        var $product_pk = $tr.attr('product-pk');
        $.post('/car-remove-product/',{'product_pk':$product_pk},function(response){
            if(response.success){
                $tr.fadeOut();
            }else{
                alert(response.message);
            }
        })
    });

    $('.update-quantity').focusout(function(e){
        e.preventDefault();
        var $generateServiceOrder = $('#generateServiceOrder');
        $generateServiceOrder.attr('disabled','disabled');
        var $tr= $(this).parents('tr');
        var $product_pk = $tr.attr('product-pk');
        var quantity = $(this).val();
        if($.isNumeric(quantity)){
            $.post('/car-update-product/',{'product_pk':$product_pk, 'quantity':quantity},function(response){
                if(response.success){
                    $generateServiceOrder.removeAttr('disabled');
                }else{
                    alert(response.message);
                }
            });
        }else{
            $(this).val('')
            $(this).focus();
//            alert('Porfavor, ingresa un numero correcto');
        }
    });

});