import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const getById = mutation({
  args: {
    id: v.id("updated_userprofile")
  },
  handler: async (ctx, args) => {
    return await ctx.db.query("updated_userprofile")
      .filter(q => q.eq(q.field("_id"), args.id))
      .collect();
  },
});

export const getByUserId = mutation({
  args: {
    user_id: v.id("updated_users")
  },
  handler: async (ctx, args) => {
    let result = await ctx.db.query("updated_userprofile")
      .filter(q => q.eq(q.field("user_id"), args.user_id))
      .unique();
    if (result.length) {
      return { success: true, result };
    } else {
      return { success: false, result: null };
    }
  },
});

export const getByEmailToken = mutation({
  args: {
    id: v.id("updated_userprofile"),
    token: v.string()
  },
  handler: async (ctx, args) => {
    const result = await ctx.db.query("updated_userprofile")
      .filter(q => q.eq(q.field("_id"), args.id))
      .filter(q => q.eq(q.field("confirmation_email_token"), args.token))
      .collect();

    if (result.length) {
      return { success: true, result };
    } else {
      return { success: false, result: null };
    }
  },
});

export const getByPhoneCode = mutation({
  args: {
    id: v.id("updated_userprofile"),
    confirmation_phone_code: v.string()
  },
  handler: async (ctx, args) => {
    const result = await ctx.db.query("updated_userprofile")
      .filter(q => q.eq(q.field("_id"), args.id))
      .filter(q => q.eq(q.field("confirmation_phone_code"), args.confirmation_phone_code))
      .collect();

    if (result.length) {
      return { success: true, result };
    } else {
      return { success: false, result: null };
    }
  },
});

export const getByPhoneNumber = mutation({
  args: { phone_number: v.string() },
  handler: async (ctx, args) => {
    const result = await ctx.db.query("updated_userprofile")
      .filter(q => q.eq(q.field("phone_number"), args.phone_number))
      .collect();

    if (result.length) {
      return { success: true, result };
    } else {
      return { success: false, result: null };
    }
  },
});

export const updateProfile = mutation({
  args: {
    avatar: v.string(),
    bio: v.string(),
    birthday: v.string(),
    display_name: v.string(),
    privacy_level: v.string(),
    gender: v.string(),
    last_reset: v.string(),
    location: v.string(),
    phone_number: v.string(),
    user_id: v.id("updated_users"),
  },
  handler: async (ctx, args) => {
    let result;

    const exist_user_profile = await ctx.db
      .query("updated_userprofile")
      .filter(q => q.eq(q.field("user_id"), args.user_id))
      .collect();
    const id = exist_user_profile[0]?._id;
    if (id) {
      await ctx.db.patch(id, {
        avatar: args.avatar,
        bio: args.bio,
        birthday: args.birthday,
        display_name: args.display_name,
        privacy_level: args.privacy_level,
        last_reset: args.last_reset,
        gender: args.gender,
        location: args.location,
        phone_number: args.phone_number
      });
      result = id;
    } else {
      result = await ctx.db
        .insert("updated_userprofile", {
          avatar: args.avatar,
          bio: args.bio,
          birthday: args.birthday,
          display_name: args.display_name,
          privacy_level: args.privacy_level,
          last_reset: args.last_reset,
          gender: args.gender,
          location: args.location,
          phone_number: args.phone_number,
          user_id: args.user_id
        });
    }

    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to update or insert profile." };
    }
  },
});

export const updateSecurity = mutation({
  args: {
    auto_approve_friend_request: v.boolean(),
    hide_online_status: v.boolean(),
    visibility: v.string(),
    user_id: v.id("updated_users"),
  },
  handler: async (ctx, args) => {
    let result;

    const exist_user_profile = await ctx.db
      .query("updated_userprofile")
      .filter(q => q.eq(q.field("user_id"), args.user_id))
      .collect();
    const id = exist_user_profile[0]?._id;
    if (id) {
      await ctx.db.patch(id, {
        auto_approve_friend_request: args.auto_approve_friend_request,
        hide_online_status: args.hide_online_status,
        visibility: args.visibility
      });
      result = id;
    } else {
      result = await ctx.db
        .insert("updated_userprofile", {
          auto_approve_friend_request: args.auto_approve_friend_request,
          hide_online_status: args.hide_online_status,
          visibility: args.visibility,
          user_id: args.user_id
        });
    }

    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to update or insert security info." };
    }
  },
});

export const updateNotificationSetting = mutation({
  args: {
    notificationRecieveConfig: v.string(),
    user_id: v.id("updated_users"),
  },
  handler: async (ctx, args) => {
    let result;

    const exist_user_profile = await ctx.db
      .query("updated_userprofile")
      .filter(q => q.eq(q.field("user_id"), args.user_id))
      .collect();
    const id = exist_user_profile[0]?._id;
    if (id) {
      await ctx.db.patch(id, {
        notificationRecieveConfig: args.notificationRecieveConfig
      });
      result = id;
    } else {
      result = await ctx.db
        .insert("updated_userprofile", {
          notificationRecieveConfig: args.notificationRecieveConfig,
          user_id: args.user_id
        });
    }
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to update or insert notification setting." };
    }
  },
});

export const updateEnableNotification = mutation({
  args: {
    enable_notification: v.boolean(),
    user_id: v.id("updated_users"),
  },
  handler: async (ctx, args) => {
    let result;

    const exist_user_profile = await ctx.db
      .query("updated_userprofile")
      .filter(q => q.eq(q.field("user_id"), args.user_id))
      .collect();
    const id = exist_user_profile[0]?._id;
    if (id) {
      await ctx.db.patch(id, {
        enable_notification: args.enable_notification
      });
      result = id;
    } else {
      result = await ctx.db
        .insert("updated_userprofile", {
          enable_notification: args.enable_notification,
          user_id: args.user_id
        });
    }
    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to update or insert enable notification flag." };
    }
  },
});

export const generateConfirmToken = mutation({
  args: {
    confirmation_email_token: v.string(),
    phone_number: v.string(),
    email_expire_at: v.string(),
    user_id: v.id('updated_users'),
  },
  handler: async (ctx, args) => {
    let result;

    const exist_user_profile = await ctx.db
      .query("updated_userprofile")
      .filter(q => q.eq(q.field("user_id"), args.user_id))
      .collect();
    const id = exist_user_profile[0]?._id;
    if (id) {
      await ctx.db.patch(id, {
        confirmation_email_token: args.confirmation_email_token,
        email_confirmed: false,
        phone_number: args.phone_number,
        phone_confirmed: false,
        email_expire_at: args.email_expire_at
      });
      result = id;
    } else {
      result = await ctx.db
        .insert("updated_userprofile", {
          confirmation_email_token: args.confirmation_email_token,
          phone_number: args.phone_number,
          email_confirmed: false,
          phone_confirmed: false,
          email_expire_at: args.email_expire_at,
          user_id: args.user_id
        });
    }

    if (result) {
      return { success: true, result };
    } else {
      return { success: false, result: "Failed to update or insert profile." };
    }
  },
});

export const verifiedEmail = mutation({
  args: {
    confirmation_phone_code: v.string(),
    phone_expire_at: v.string(),
    id: v.id("updated_userprofile")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      email_confirmed: true,
      phone_confirmed: false,
      phone_expire_at: args.phone_expire_at,
      confirmation_phone_code: args.confirmation_phone_code
    });
    return { success: true, result: args.id };
  },
});

export const verifiedPhone = mutation({
  args: {
    id: v.id("updated_userprofile")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      phone_confirmed: true,
      confirmation_phone_code: ""
    });
    return { success: true, result: args.id };
  },
});

export const generateRecreateConfirmToken = mutation({
  args: {
    confirmation_email_token: v.string(),
    email_expire_at: v.string(),
    id: v.id("updated_userprofile")
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.id, {
      confirmation_email_token: args.confirmation_email_token,
      email_confirmed: false,
      phone_confirmed: false,
      email_expire_at: args.email_expire_at
    });
    return { success: true, result: args.id };
  },
});