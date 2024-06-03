import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const getById = mutation({
  args: {
    id: v.id("updated_friends")
  },
  handler: async (ctx, args) => {
    return await ctx.db.query("updated_friends")
      .filter(q => q.eq(q.field("_id"), args.id))
      .collect();
  },
});

export const followOrUnfollow = mutation({
  args: {
    user_id: v.id("updated_users"),
    follower_id: v.float64(),
  },
  handler: async (ctx, args) => {
    const existingFollow = await ctx.db
      .query("updated_followers")
      .filter(q => q.eq(q.field("user_id"), args.user_id))
      .filter(q => q.eq(q.field("follower_id"), args.follower_id))
      .collect();

    if (existingFollow.length) {
      await ctx.db.delete(existingFollow[0]._id);
      return { success: true, result: "Unfollowed successfully" };
    } else {
      const result = await ctx.db.insert("updated_followers", {
        user_id: args.user_id,
        follower_id: args.follower_id,
      });

      if (result) {
        return { success: true, result: "Followed successfully" };
      } else {
        return { success: false, result: "Failed to follow" };
      }
    }
  },
});