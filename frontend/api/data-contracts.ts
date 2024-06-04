/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/**
 * HTTPValidationError
 */
export interface HTTPValidationError {
  /**
   * Detail
   */
  detail?: ValidationError[];
}

/**
 * Response
 */
export interface Response {
  /**
   * Message
   */
  message: string;
}

/**
 * UserRequest
 */
export interface UserRequest {
  /**
   * Email
   */
  email: string;

  /**
   * Name
   */
  name: string | null;

  /**
   * Organization
   */
  organization: string | null;
}

/**
 * UserResponse
 */
export interface UserResponse {
  /**
   * Id
   */
  id: string;

  /**
   * Email
   */
  email: string;

  /**
   * Name
   */
  name: string;

  /**
   * Organization Name
   */
  organization_name: string;

  /**
   * Is Internal
   */
  is_internal: boolean;

  /**
   * Profile Image
   */
  profile_image: string | null;

  status: UserStatus;

  /**
   * Created At
   *
   * @format date-time
   */
  created_at: string;

  /**
   * Updated At
   *
   * @format date-time
   */
  updated_at: string;
}

/**
 * UserStatus
 */
export enum UserStatus {
  ACTIVE = "ACTIVE",
  PENDING = "PENDING",
  DEACTIVATED = "DEACTIVATED",
}

/**
 * ValidationError
 */
export interface ValidationError {
  /**
   * Location
   */
  loc: (string | number)[];

  /**
   * Message
   */
  msg: string;

  /**
   * Error Type
   */
  type: string;
}
