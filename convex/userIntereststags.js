import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  handler: async (ctx) => {
    if (!ctx) return;
    return await ctx.db.query("updated_intereststags").collect();
  },
});

export const insertUserInterestsTags = mutation({
  args: {
    user_id: v.id("updated_users"),
    id: v.id("updated_intereststags"),
  },
  handler: async (ctx, args) => {
    let result = await ctx.db
      .insert("updated_userintereststags", {
        interestsTags_id: args.id,
        user_id: args.user_id
      });
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to insert user interests tag." };
    }
  },
});