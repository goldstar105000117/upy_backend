import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  handler: async (ctx) => {
    return await ctx.db.query("updated_customstatus").collect();
  },
});

export const insertCustomStatus = mutation({
  args: {
    message: v.string(),
    icon: v.string(),
  },
  handler: async (ctx, args) => {
    let result = await ctx.db
      .insert("updated_customstatus", {
        message: args.message,
        icon: args.icon
      });
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to insert custom status." };
    }
  },
});

export const updateCustomStatus = mutation({
  args: {
    message: v.string(),
    icon: v.string(),
    id: v.id("updated_customstatus")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      message: args.message,
      icon: args.icon
    });
    let result = args.id;
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to update status." };
    }
  },
});

export const deleteCustomStatus = mutation({
  args: {
    id: v.id("updated_customstatus")
  },
  handler: async (ctx, args) => {
    return await ctx.db.delete(args.id);
  },
});