# pr0gramm-comments
Service to store comment favorites.

## Client
This is a simple javascript client using jQuery.
```javascript
var CommentFavorites = {
  list: function(user_hash) {
    return jQuery.ajax({
        method: "GET",
        url: "http://pr0.wibbly-wobbly.de/api/comments/v1/" + encodeURIComponent(user_hash)
    });
  },

  put: function(user_hash, item_id, comment) {
    var body = jQuery.extend({}, comment, {item_id: item_id});
    return jQuery.ajax({
      method: "POST",
      url: "http://pr0.wibbly-wobbly.de/api/comments/v1/" + encodeURIComponent(user_hash),
      contentType: "application/json",
      data: JSON.stringify(body)
    });
  },

  delete: function(user_hash, comment_id) {
    return jQuery.ajax({
      method: "POST",
      url: "http://pr0.wibbly-wobbly.de/api/comments/v1/" + encodeURIComponent(user_hash) + "/" + encodeURIComponent(comment_id) + "/delete"
    });
  }
};
```

A comment object must contain the following properties: `id`, `name`, `content`,
`up`, `down`, `mark` as well as the creation time `created` in seconds. Those values are
exactly the same as on a pr0gramm comment object.

Examples:
```javascript
var user = someMd5HashLibrary.hash(info.user.email);
var comment = {id: 42, name: "Mopsalarm", content: "Testkommentar", up:20, down:10, mark:0, created: 1448092867};
var item_id = 771552;

CommentFavorites.put(user, item_id, comment).then(function() {
  console.log("Comment saved");
});

CommentFavorites.list(user).then(function(comments) {
  console.log("Comments: ", comments);
});

CommentFavorites.delete(user, comment.id).then(function() {
  console.log("Comment deleted");
});
```
