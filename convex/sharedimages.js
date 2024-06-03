import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  handler: async (ctx) => {
    if (!ctx) return;
    return await ctx.db.query("updated_sharedimages").collect();
  },
});

export const insertSharedImages = mutation({
  args: {
    user_id: v.id("updated_users"),
    image: v.string(),
  },
  handler: async (ctx, args) => {
    let result = await ctx.db
      .insert("updated_sharedimages", {
        user_id: args.user_id,
        image: args.image
      });
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to insert shared image." };
    }
  },
});

export const updateSharedImages = mutation({
  args: {
    image: v.string(),
    id: v.id("updated_sharedimages")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      image: args.image
    });
    let result = args.id;
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to update shared image." };
    }
  },
});

export const deleteSharedImages = mutation({
  args: {
    id: v.id("updated_sharedimages")
  },
  handler: async (ctx, args) => {
    return await ctx.db.delete(args.id);
  },
});