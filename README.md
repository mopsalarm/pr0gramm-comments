# pr0gramm-comments
Service to store comment favorites.

## Client
This is a simple javascript client using jQuery.
```javascript

var CommentFavorites = {
  list: function(user_hash, flags) {
    return jQuery.ajax({
        method: "GET",
        url: "//pr0.wibbly-wobbly.de/api/comments/v1/" + encodeURIComponent(user_hash),
        data: {flags: flags || 1}
    });
  },

  put: function(user_hash, item_id, comment) {
    var body = jQuery.extend({}, comment, {item_id: item_id});
    return jQuery.ajax({
      method: "POST",
      url: "//pr0.wibbly-wobbly.de/api/comments/v1/" + encodeURIComponent(user_hash),
      contentType: "application/json",
      data: JSON.stringify(body)
    });
  },

  delete: function(user_hash, comment_id) {
    return jQuery.ajax({
      method: "POST",
      url: "//pr0.wibbly-wobbly.de/api/comments/v1/" + encodeURIComponent(user_hash) + "/" + encodeURIComponent(comment_id) + "/delete"
    });
  }
};
```

A comment object must contain the following properties: `id`, `name`, `content`,
`up`, `down`, `mark`, `thumb` as well as the creation time `created` in seconds. Those values are
exactly the same as on a pr0gramm comment object.

Examples:
```javascript
var user = someMd5HashLibrary.hash(info.user.email);
var comment = {id: 42, name: "Mopsalarm", content: "Testkommentar", up:20, down:10, mark:0, created: 1448092867, thumb: "2015/11/21/2b37cf2e3f9774a4.jpg", flags: 1};
var item_id = 771552;

CommentFavorites.put(user, item_id, comment).then(function() {
  console.log("Comment saved");
});

var flags = 1; // bit combination of 1, 2, 4
CommentFavorites.list(user, flags).then(function(comments) {
  console.log("Comments: ", comments);
});

CommentFavorites.delete(user, comment.id).then(function() {
  console.log("Comment deleted");
});
```
