$(document).ready(function(){
    $('.increase').click(function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.product_data').find('.quantity').val();
        var value= parseInt(inc_value,10);
        value = isNaN(value) ? 0: value;
        if (value < 10) {
            value++;
            $(this).closest('.product_data').find('.quantity').val(value);
        }
    });
    $('.decrease').click(function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.product_data').find('.quantity').val();
        var value= parseInt(dec_value,10);
        value = isNaN(value) ? 0: value;
        if (value > 1) {
            value--;
            $(this).closest('.product_data').find('.quantity').val(value);
        }
    });
    $('.addtocartbtn').click(function (e) { 
        e.preventDefault();
        
        var product_id =  $(this).closest('.product_data').find('.prod_id').val();
        var product_qty =  $(this).closest('.product_data').find('.quantity').val();
        var token= $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url:'/add-to-cart',
            data:{
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function(response){
                console.log(response)
                alertify.success(response.status)
            }

        });
    });
    $('.addtowishlistbtn').click(function (e) { 
        e.preventDefault();
        
        var product_id =  $(this).closest('.product_data').find('.prod_id').val();
        var token= $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url:'/add-to-wishlist',
            data:{
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function(response){
                alertify.success(response.status)
            }

        });
    });
    $('.delete-cart-item').click(function (e) { 
        e.preventDefault();
        
        var product_id =  $(this).closest('.product_data').find('.prod_id').val();
        var token= $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url:'/delete-cart-item',
            data:{
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function(response){
                if (response.status === "deleted successfully") {
                    $(e.target).closest('.product_data').remove();
                    alertify.success(response.status)
                    if ($('.product_data').length === 0) {
                        $('.cartbody').html('<h1 id="ciem">Your Cart is Empty</h1><center><img src="/static/images/emptycart.png" alt="" width="500px" ></center>');
                    }
                } else {
                    alertify.error("Error occurred while deleting item.");
                }
            }

        });
    });
    $(document).ready(function () {
        // Event handler for deleting wishlist items
        $('.delete-wishlist-item').click(function (e) {
            e.preventDefault();
    
            var deleteButton = $(this);
            var wishcard = deleteButton.closest('.wishcard');
            var product_id = wishcard.find('.prod_id').val();
            var token = $('input[name=csrfmiddlewaretoken]').val();
    
            $.ajax({
                method: 'POST',
                url: '/delete-wishlist-item',
                data: {
                    'product_id': product_id,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    if (response.status === "deleted from wishlist successfully") {
                        wishcard.remove();
                        alertify.success(response.status);
                        if ($('.wishcard').length === 0) {
                            $('.wishbody').html('<h1 id="wiem">is Empty</h1>');
                        }
                    } else {
                        alertify.error("Error occurred while deleting item.");
                    }
                },
                
            });
        });
    });
    
    $('.changeQuantity').click(function (e) { 
        e.preventDefault();
        
        var product_id =  $(this).closest('.product_data').find('.prod_id').val();
        var product_qty =  $(this).closest('.product_data').find('.quantity').val();
        var token= $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url:'/update-cart',
            data:{
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function(response){
                // alertify.success(response.status)
            }

        });
    });
});