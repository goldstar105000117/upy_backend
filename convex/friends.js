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

export const requestFriend = mutation({
  args: {
    friend_id: v.float64(),
    user_id: v.id("updated_users"),
  },
  handler: async (ctx, args) => {
    let result = await ctx.db
      .insert("updated_friends", {
        friend_id: args.friend_id,
        status: "pending",
        user_id: args.user_id
      });
    
    return { success: true, result };
  },
});

export const approveFriendRequest = mutation({
  args: {
    id: v.id("updated_friends")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      status: "approved"
    });
    return { success: true, result: args.id };
  },
});

export const declineFriendRequest = mutation({
  args: {
    id: v.id("updated_friends")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      status: "declined"
    });
    return { success: true, result: args.id };
  },
});