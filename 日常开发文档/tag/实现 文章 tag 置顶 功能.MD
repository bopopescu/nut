1.  ADD a new FIELD in Tags Model , 
     new field : 
        isTopArticleTag , BooleanField
        
      
2.  RUN ALert table SQL 
 
ALTER TABLE `core`.`tag_tags` 
ADD COLUMN `isTopArticleTag` TINYINT(1) NOT NULL DEFAULT 0 AFTER `image`;



3.  add a switchery component to tag list management page 
http://abpetkov.github.io/switchery/

3.5  init switchery component state when render template

4.  hook switch change event to ajax call to a background view to handle the state change 
    the ajax call will get a state for tag , you should change the switchery component base 
    on the returned value , to fully keep sync between data and presentation
    
    
5.  use select_related('TagState') to reduce query

6.  sort by  tagstate to find switched tag quickly 

