db.articles.aggregate([
  {
    $unwind: "$categories", // Unwind the categories array to consider each category separately
  },
  {
    $group: {
      _id: "$categories", // Group by category
      count: { $sum: 1 }, // Count the number of articles in each category
    },
  },
  {
    $sort: { _id: 1 }, // Sort the results by category (_id) in ascending order
  },
]);
