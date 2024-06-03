import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const getByIdAndToken = mutation({
    args: {
        id: v.id("updated_tokens"),
        token: v.string()
    },
    handler: async (ctx, args) => {
        const result = await ctx.db.query("updated_tokens")
            .filter(q => q.eq(q.field("_id"), args.id))
            .filter(q => q.eq(q.field("token"), args.token))
            .collect();
            
        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: "Failed to get token." };
        }
    },
});

export const getByTokenAndTypeAndUserId = mutation({
    args: {
        token: v.string(),
        user_id: v.id("updated_users"),
        type: v.string()
    },
    handler: async (ctx, args) => {
        let result = await ctx.db.query("updated_tokens")
            .filter(q => q.eq(q.field("user_id"), args.user_id))
            .filter(q => q.eq(q.field("token"), args.token))
            .filter(q => q.eq(q.field("type"), args.type))
            .unique();

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: "Failed to fetch token." };
        }
    },
});

export const generateConfirmToken = mutation({
    args: {
        token: v.string(),
        expired_at: v.string(),
        type: v.string(),
        user_id: v.id("updated_users"),
    },
    handler: async (ctx, args) => {
        let result;

        const exist_user_profile = await ctx.db
            .query("updated_tokens")
            .filter(q => q.eq(q.field("user_id"), args.user_id))
            .filter(q => q.eq(q.field("type"), args.type))
            .collect();
        const id = exist_user_profile[0]?._id;
        if (id) {
            await ctx.db.patch(id, {
                token: args.token,
                expired_at: args.expired_at
            });
            result = id;
        } else {
            result = await ctx.db
                .insert("updated_tokens", {
                    token: args.token,
                    expired_at: args.expired_at,
                    type: args.type,
                    user_id: args.user_id
                });
        }

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: "Failed to update or insert token." };
        }
    },
});

export const deleteTokenById = mutation({
    args: {
        id: v.id("updated_tokens")
    },
    handler: async (ctx, args) => {
        await ctx.db.delete(args.id);
        return { success: true, result: args.id };
    },
});