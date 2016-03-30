
$('#index-banners').slick({


  centerMode: true,
  arrows: true,
  slidesToShow: 1,
  centerPadding:'15%',
  dots:true,

  //centerPadding: '60px',
  //slidesToShow: 3,
  responsive: [
    {
      breakpoint: 768,
      settings: {
         centerMode:false,
         slidesToShow:1,
         slidesToScroll:1,
         infinite: true
      }
    },
  ]
  //  {
  //    breakpoint: 480,
  //    settings: {
  //      arrows: false,
  //      centerMode: true,
  //      centerPadding: '40px',
  //      slidesToShow: 1
  //    }
  //  }
  //]
});