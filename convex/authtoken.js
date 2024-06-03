import { mutation, } from "./_generated/server";
import { v } from "convex/values";

export const getById = mutation({
    args: {
        id: v.id("updated_auth_tokens")
    },
    handler: async (ctx, args) => {
        return await ctx.db.query("updated_auth_tokens")
            .filter(q => q.eq(q.field("_id"), args.id))
            .collect();
    },
});

export const getByUserId = mutation({
    args: {
        user_id: v.id("updated_users")
    },
    handler: async (ctx, args) => {
        const result =  await ctx.db.query("updated_auth_tokens")
            .filter(q => q.eq(q.field("user_id"), args.user_id))
            .unique();
            
        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: null };
        }
    },
});

export const getByRefreshToken = mutation({
    args: {
        refresh_token: v.string()
    },
    handler: async (ctx, args) => {
        const result =  await ctx.db.query("updated_auth_tokens")
            .filter(q => q.eq(q.field("refresh_token"), args.refresh_token))
            .first();
            
        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: null };
        }
    },
});
export const getByAccessToken = mutation({
    args: {
        access_token: v.string()
    },
    handler: async (ctx, args) => {
        const result = await ctx.db.query("updated_auth_tokens")
            .filter(q => q.eq(q.field("access_token"), args.access_token))
            .first();
            
        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: null };
        }
    },
});

export const addToken = mutation({
    args: {
        user_id: v.id("updated_users"),
        access_token: v.string(),
        refresh_token: v.string(),
    },
    handler: async (ctx, args) => {
        const token = {
            user_id: args.user_id,
            access_token: args.access_token,
            refresh_token: args.refresh_token,
        };
        const result = await ctx.db.insert('updated_auth_tokens', token);

        if (result) {
            return { success: true, result };
        } else {
            return { success: false, result: "Failed insert token." };
        }
    },
});

export const updateToken = mutation({
    args: {
        id: v.id("updated_auth_tokens"),
        access_token: v.string(),
        refresh_token: v.string(),
    },
    handler: async (ctx, args) => {
        await ctx.db.patch(args.id, {
            access_token: args.access_token,
            refresh_token: args.refresh_token,
        });
        return { success: true, result: args.id };
    },
});

export const updateTokenBtRefreshToken = mutation({
    args: {
        refresh_token: v.string(),
        access_token: v.string(),
    },
    handler: async (ctx, args) => {
        const token = await ctx.db.query("updated_auth_tokens")
            .filter(q => q.eq(q.field("refresh_token"), args.refresh_token))
            .first();
        if (token) {
            await ctx.db.patch(token._id, {
                access_token: args.access_token,
            });
            return { success: true, result: token._id };
        } else {
            return { success: false, result: "Token not found." };
        }
    },
});

export const deleteToken = mutation({
    args: {
        id: v.id("updated_auth_tokens"),
    },
    handler: async (ctx, args) => {
        await ctx.db.delete(args.id);
        return { success: true, result: args.id };
    },
});

export const deleteTokenByUserId = mutation({
    args: {
        user_id: v.id("updated_users"),
    },
    handler: async (ctx, args) => {
        const token = await ctx.db.query("updated_auth_tokens")
            .filter(q => q.eq(q.field("user_id"), args.user_id))
            .first();
        if (token) {
            await ctx.db.delete(token._id);
            return { success: true, result: token._id };
        } else {
            return { success: false, result: "Token not found." };
        }
    },
});

export const deleteTokenByRefreshToken = mutation({
    args: {
        refresh_token: v.string(),
    },
    handler: async (ctx, args) => {
        const token = await ctx.db.query("updated_auth_tokens")
            .filter(q => q.eq(q.field("refresh_token"), args.refresh_token))
            .first();
        if (token) {
            await ctx.db.delete(token._id);
            return { success: true, result: token._id };
        } else {
            return { success: false, result: "Token not found." };
        }
    },
});