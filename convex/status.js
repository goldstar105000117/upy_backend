import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  handler: async (ctx) => {
    return await ctx.db.query("updated_status").collect();
  },
});

export const insertStatus = mutation({
  args: {
    name: v.string(),
    icon: v.string(),
  },
  handler: async (ctx, args) => {
    let result = await ctx.db
      .insert("updated_status", {
        name: args.name,
        icon: args.icon
      });
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to insert status." };
    }
  },
});

export const updateStatus = mutation({
  args: {
    name: v.string(),
    icon: v.string(),
    id: v.id("updated_status")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      name: args.name,
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

export const deleteStatus = mutation({
  args: {
    id: v.id("updated_status")
  },
  handler: async (ctx, args) => {
    return await ctx.db.delete(args.id);
  },
});